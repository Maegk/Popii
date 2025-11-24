"""
Learning Engine

Learns which creative elements work for specific audiences and auto-generates new combinations.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np
from loguru import logger

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.creative import Creative, CreativeFormat
from src.models.creative_performance import CreativePerformance
from src.models.audience_insight import AudienceInsight
from src.config import settings


class LearningEngine:
    """Learns from creative performance data"""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def update_audience_insights(
        self,
        segment_id: str,
        segment_name: str,
    ) -> AudienceInsight:
        """
        Update audience insights based on recent performance data

        Args:
            segment_id: Audience segment ID
            segment_name: Audience segment name

        Returns:
            Updated AudienceInsight object
        """
        logger.info(f"Updating audience insights for segment: {segment_id}")

        # Get existing insight or create new
        query = select(AudienceInsight).where(AudienceInsight.segment_id == segment_id)
        result = await self.db.execute(query)
        insight = result.scalar_one_or_none()

        if not insight:
            insight = AudienceInsight(
                segment_id=segment_id,
                segment_name=segment_name,
            )
            self.db.add(insight)

        # Gather performance data for this segment
        performance_data = await self._get_segment_performance(segment_id)

        if len(performance_data) < settings.min_samples_for_learning:
            logger.warning(
                f"Insufficient data for segment {segment_id}: "
                f"{len(performance_data)} samples (minimum: {settings.min_samples_for_learning})"
            )
            insight.confidence_score = 0.0
            await self.db.commit()
            return insight

        # Analyze performance patterns
        insights_data = self._analyze_performance_patterns(performance_data)

        # Update insight object
        insight.preferred_format = insights_data.get("preferred_format")
        insight.preferred_hook_type = insights_data.get("preferred_hook_type")
        insight.preferred_tone = insights_data.get("preferred_tone")
        insight.avg_ctr = insights_data.get("avg_ctr", 0.0)
        insight.avg_cpa = insights_data.get("avg_cpa", 0.0)
        insight.avg_engagement_rate = insights_data.get("avg_engagement_rate", 0.0)
        insight.avg_fatigue_threshold_days = insights_data.get(
            "avg_fatigue_threshold_days", 7.0
        )
        insight.frequency_tolerance = insights_data.get("frequency_tolerance", 6.0)
        insight.sample_size = len(performance_data)
        insight.confidence_score = self._calculate_confidence(len(performance_data))
        insight.top_hooks = insights_data.get("top_hooks", [])
        insight.top_angles = insights_data.get("top_angles", [])
        insight.top_ctas = insights_data.get("top_ctas", [])
        insight.last_updated_samples = len(performance_data)

        await self.db.commit()
        await self.db.refresh(insight)

        logger.info(
            f"Updated insights for {segment_id}: "
            f"confidence={insight.confidence_score:.2f}, samples={insight.sample_size}"
        )

        return insight

    async def _get_segment_performance(
        self,
        segment_id: str,
        days: int = 90,
    ) -> List[Dict[str, Any]]:
        """Get performance data for a segment"""
        start_date = datetime.now() - timedelta(days=days)

        # Query creative performance with audience metadata
        query = (
            select(CreativePerformance, Creative)
            .join(Creative, Creative.id == CreativePerformance.creative_id)
            .where(CreativePerformance.date >= start_date)
        )

        result = await self.db.execute(query)
        rows = result.all()

        # Filter by segment (from audience_metadata JSON field)
        segment_data = []
        for perf, creative in rows:
            if perf.audience_metadata and perf.audience_metadata.get("segment_id") == segment_id:
                segment_data.append(
                    {
                        "creative": creative,
                        "performance": perf,
                        "ctr": perf.ctr,
                        "cpa": perf.cpa,
                        "engagement_rate": perf.engagement_rate,
                        "performance_score": perf.performance_score,
                        "format": creative.format,
                        "headline": creative.headline,
                        "body_text": creative.body_text,
                        "call_to_action": creative.call_to_action,
                    }
                )

        return segment_data

    def _analyze_performance_patterns(
        self,
        performance_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Analyze performance data to extract insights"""
        if not performance_data:
            return {}

        # Aggregate metrics
        ctrs = [d["ctr"] for d in performance_data if d["ctr"] > 0]
        cpas = [d["cpa"] for d in performance_data if d["cpa"] > 0]
        engagement_rates = [d["engagement_rate"] for d in performance_data]

        avg_ctr = float(np.mean(ctrs)) if ctrs else 0.0
        avg_cpa = float(np.mean(cpas)) if cpas else 0.0
        avg_engagement = float(np.mean(engagement_rates)) if engagement_rates else 0.0

        # Find preferred format (highest avg performance score)
        format_scores = defaultdict(list)
        for d in performance_data:
            fmt = d["format"].value if hasattr(d["format"], "value") else str(d["format"])
            format_scores[fmt].append(d.get("performance_score", 0))

        preferred_format = None
        if format_scores:
            avg_format_scores = {
                fmt: np.mean(scores) for fmt, scores in format_scores.items()
            }
            preferred_format = max(avg_format_scores, key=avg_format_scores.get)

        # Analyze headlines for hook types
        hook_analysis = self._analyze_hooks([d.get("headline", "") for d in performance_data])

        # Analyze CTAs
        cta_performance = defaultdict(list)
        for d in performance_data:
            if d.get("call_to_action"):
                cta_performance[d["call_to_action"]].append(d.get("performance_score", 0))

        top_ctas = sorted(
            [
                {"cta": cta, "avg_score": float(np.mean(scores))}
                for cta, scores in cta_performance.items()
            ],
            key=lambda x: x["avg_score"],
            reverse=True,
        )[:5]

        # Estimate fatigue threshold
        # TODO: Implement actual fatigue pattern analysis
        avg_fatigue_threshold = 7.0  # Default

        return {
            "avg_ctr": avg_ctr,
            "avg_cpa": avg_cpa,
            "avg_engagement_rate": avg_engagement,
            "preferred_format": preferred_format,
            "preferred_hook_type": hook_analysis.get("top_hook_type"),
            "preferred_tone": self._detect_tone(performance_data),
            "avg_fatigue_threshold_days": avg_fatigue_threshold,
            "frequency_tolerance": 6.0,  # Default
            "top_hooks": hook_analysis.get("top_hooks", [])[:5],
            "top_angles": [],  # TODO: Implement angle analysis
            "top_ctas": top_ctas,
        }

    def _analyze_hooks(self, headlines: List[str]) -> Dict[str, Any]:
        """Analyze headlines to determine hook types"""
        hook_types = {
            "question": 0,
            "stat": 0,
            "problem": 0,
            "story": 0,
            "direct": 0,
        }

        for headline in headlines:
            if not headline:
                continue

            headline_lower = headline.lower()

            if "?" in headline:
                hook_types["question"] += 1
            elif any(word in headline_lower for word in ["%", "x", "times", "increase", "decrease"]):
                hook_types["stat"] += 1
            elif any(word in headline_lower for word in ["struggling", "tired", "problem", "issue"]):
                hook_types["problem"] += 1
            elif any(word in headline_lower for word in ["story", "once", "when", "imagine"]):
                hook_types["story"] += 1
            else:
                hook_types["direct"] += 1

        top_hook_type = max(hook_types, key=hook_types.get) if hook_types else "direct"

        return {
            "top_hook_type": top_hook_type,
            "hook_distribution": hook_types,
            "top_hooks": [h for h in headlines if h][:5],
        }

    def _detect_tone(self, performance_data: List[Dict[str, Any]]) -> str:
        """Detect preferred tone from creative text"""
        # Simple tone detection based on keywords
        tones = {
            "professional": 0,
            "casual": 0,
            "urgent": 0,
            "educational": 0,
        }

        for d in performance_data:
            body_text = d.get("body_text", "").lower()

            if any(word in body_text for word in ["proven", "expert", "professional", "certified"]):
                tones["professional"] += 1
            if any(word in body_text for word in ["hey", "awesome", "cool", "amazing"]):
                tones["casual"] += 1
            if any(word in body_text for word in ["now", "today", "limited", "hurry"]):
                tones["urgent"] += 1
            if any(word in body_text for word in ["learn", "discover", "understand", "master"]):
                tones["educational"] += 1

        return max(tones, key=tones.get) if tones else "professional"

    def _calculate_confidence(self, sample_size: int) -> float:
        """Calculate confidence score based on sample size"""
        # Confidence increases with sample size, plateaus at min_samples_for_learning * 2
        max_samples = settings.min_samples_for_learning * 2
        confidence = min(sample_size / max_samples, 1.0)
        return confidence

    async def get_recommendations(
        self,
        ad_set_id: int,
        audience_segment: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get AI-powered recommendations for creative strategy

        Args:
            ad_set_id: Ad set ID
            audience_segment: Optional audience segment

        Returns:
            List of recommendations
        """
        recommendations = []

        # Get audience insights if available
        if audience_segment:
            query = select(AudienceInsight).where(
                AudienceInsight.segment_id == audience_segment
            )
            result = await self.db.execute(query)
            insight = result.scalar_one_or_none()

            if insight and insight.confidence_score > 0.5:
                # High-confidence recommendations
                if insight.preferred_format:
                    recommendations.append(
                        {
                            "type": "format",
                            "recommendation": f"Use {insight.preferred_format} format",
                            "reason": f"This audience responds best to {insight.preferred_format} ads",
                            "confidence": insight.confidence_score,
                        }
                    )

                if insight.preferred_hook_type:
                    recommendations.append(
                        {
                            "type": "hook",
                            "recommendation": f"Use {insight.preferred_hook_type} hooks",
                            "reason": f"This audience engages more with {insight.preferred_hook_type} style hooks",
                            "confidence": insight.confidence_score,
                        }
                    )

                if insight.top_ctas:
                    top_cta = insight.top_ctas[0]
                    recommendations.append(
                        {
                            "type": "cta",
                            "recommendation": f"Use CTA: {top_cta}",
                            "reason": "Top performing CTA for this audience",
                            "confidence": insight.confidence_score,
                        }
                    )

        # General recommendations
        recommendations.append(
            {
                "type": "rotation",
                "recommendation": "Rotate creatives every 7-10 days",
                "reason": "Prevents creative fatigue and maintains performance",
                "confidence": 0.9,
            }
        )

        return recommendations
