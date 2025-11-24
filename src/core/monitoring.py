"""
Metrics Monitoring System

Tracks frequency, CTR, CPA, and other key metrics in real-time.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from loguru import logger

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.ad_set import AdSet, MonitoringStatus
from src.models.metrics import Metrics
from src.config import settings


class MetricsMonitor:
    """Monitors ad performance metrics in real-time"""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def collect_metrics(
        self,
        ad_set_id: int,
        platform_data: Dict[str, Any],
    ) -> Metrics:
        """
        Collect and store metrics for an ad set

        Args:
            ad_set_id: Internal ad set ID
            platform_data: Raw data from ad platform API

        Returns:
            Created Metrics object
        """
        # Parse platform data
        metrics_data = self._parse_platform_data(platform_data)

        # Create metrics record
        metrics = Metrics(
            ad_set_id=ad_set_id,
            date=datetime.now(),
            **metrics_data,
        )

        self.db.add(metrics)
        await self.db.commit()
        await self.db.refresh(metrics)

        logger.info(
            f"Collected metrics for ad_set_id={ad_set_id}: "
            f"CTR={metrics.ctr:.2f}%, CPA=${metrics.cpa:.2f}, Frequency={metrics.frequency:.2f}"
        )

        return metrics

    def _parse_platform_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse platform-specific data into standard metrics format"""
        # Extract metrics from platform data
        impressions = int(data.get("impressions", 0))
        clicks = int(data.get("clicks", 0))
        conversions = int(data.get("conversions", 0))
        spend = float(data.get("spend", 0.0))
        reach = int(data.get("reach", 0))

        # Calculate derived metrics
        ctr = (clicks / impressions * 100) if impressions > 0 else 0.0
        cpc = (spend / clicks) if clicks > 0 else 0.0
        cpa = (spend / conversions) if conversions > 0 else 0.0
        cpm = (spend / impressions * 1000) if impressions > 0 else 0.0
        frequency = (impressions / reach) if reach > 0 else 0.0

        # Engagement metrics
        likes = int(data.get("likes", 0))
        comments = int(data.get("comments", 0))
        shares = int(data.get("shares", 0))
        total_engagement = likes + comments + shares
        engagement_rate = (total_engagement / impressions * 100) if impressions > 0 else 0.0

        # Negative feedback
        negative_feedback = int(data.get("negative_feedback", 0))
        hide_clicks = int(data.get("hide_clicks", 0))
        report_clicks = int(data.get("report_clicks", 0))

        return {
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "ctr": ctr,
            "cpc": cpc,
            "cpa": cpa,
            "cpm": cpm,
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "engagement_rate": engagement_rate,
            "frequency": frequency,
            "reach": reach,
            "spend": spend,
            "negative_feedback": negative_feedback,
            "hide_clicks": hide_clicks,
            "report_clicks": report_clicks,
        }

    async def get_current_metrics(self, ad_set_id: int) -> Optional[Metrics]:
        """Get the most recent metrics for an ad set"""
        query = (
            select(Metrics)
            .where(Metrics.ad_set_id == ad_set_id)
            .order_by(Metrics.date.desc())
            .limit(1)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_metrics_history(
        self,
        ad_set_id: int,
        days: int = 30,
    ) -> List[Metrics]:
        """Get metrics history for an ad set"""
        start_date = datetime.now() - timedelta(days=days)

        query = (
            select(Metrics)
            .where(Metrics.ad_set_id == ad_set_id)
            .where(Metrics.date >= start_date)
            .order_by(Metrics.date.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def detect_metric_anomalies(
        self,
        ad_set_id: int,
        current_metrics: Metrics,
    ) -> Dict[str, Any]:
        """
        Detect anomalies in current metrics compared to historical average

        Returns:
            Dict with anomaly flags and percentage changes
        """
        # Get historical baseline (last 7 days, excluding today)
        history = await self.get_metrics_history(ad_set_id, days=7)

        if len(history) < 3:
            return {"insufficient_data": True}

        # Calculate averages
        avg_ctr = sum(m.ctr for m in history) / len(history)
        avg_cpa = sum(m.cpa for m in history) / len(history)
        avg_engagement = sum(m.engagement_rate for m in history) / len(history)
        avg_frequency = sum(m.frequency for m in history) / len(history)

        # Calculate changes
        ctr_change = ((current_metrics.ctr - avg_ctr) / avg_ctr * 100) if avg_ctr > 0 else 0
        cpa_change = ((current_metrics.cpa - avg_cpa) / avg_cpa * 100) if avg_cpa > 0 else 0
        engagement_change = (
            (current_metrics.engagement_rate - avg_engagement) / avg_engagement * 100
            if avg_engagement > 0
            else 0
        )
        frequency_change = (
            (current_metrics.frequency - avg_frequency) / avg_frequency * 100
            if avg_frequency > 0
            else 0
        )

        # Detect anomalies based on thresholds
        anomalies = {
            "ctr_drop": ctr_change < -settings.fatigue_ctr_drop_percent,
            "ctr_change_percent": ctr_change,
            "cpa_increase": cpa_change > settings.fatigue_cpa_increase_percent,
            "cpa_change_percent": cpa_change,
            "engagement_drop": engagement_change < -settings.fatigue_engagement_drop_percent,
            "engagement_change_percent": engagement_change,
            "high_frequency": current_metrics.frequency > settings.fatigue_frequency_threshold,
            "frequency_change_percent": frequency_change,
            "has_anomaly": False,
        }

        # Set has_anomaly flag
        anomalies["has_anomaly"] = any(
            [
                anomalies["ctr_drop"],
                anomalies["cpa_increase"],
                anomalies["engagement_drop"],
                anomalies["high_frequency"],
            ]
        )

        return anomalies

    async def should_trigger_alert(
        self,
        ad_set_id: int,
        anomalies: Dict[str, Any],
    ) -> bool:
        """
        Determine if anomalies warrant an alert

        Args:
            ad_set_id: Ad set ID
            anomalies: Anomaly detection results

        Returns:
            True if alert should be triggered
        """
        if not anomalies.get("has_anomaly"):
            return False

        # Get current metrics
        current = await self.get_current_metrics(ad_set_id)
        if not current:
            return False

        # Check if we have enough impressions for reliable analysis
        if current.impressions < settings.min_impressions_for_analysis:
            return False

        # Multiple red flags = definite alert
        red_flags = sum(
            [
                anomalies.get("ctr_drop", False),
                anomalies.get("cpa_increase", False),
                anomalies.get("engagement_drop", False),
                anomalies.get("high_frequency", False),
            ]
        )

        return red_flags >= 2  # At least 2 red flags

    async def get_monitoring_status(self, ad_set_id: int) -> Dict[str, Any]:
        """Get comprehensive monitoring status for an ad set"""
        # Get ad set
        query = select(AdSet).where(AdSet.id == ad_set_id)
        result = await self.db.execute(query)
        ad_set = result.scalar_one_or_none()

        if not ad_set:
            return {"error": "Ad set not found"}

        # Get current metrics
        current_metrics = await self.get_current_metrics(ad_set_id)

        if not current_metrics:
            return {
                "ad_set_id": ad_set_id,
                "status": "no_data",
                "message": "No metrics collected yet",
            }

        # Detect anomalies
        anomalies = await self.detect_metric_anomalies(ad_set_id, current_metrics)

        # Check if alert should trigger
        should_alert = await self.should_trigger_alert(ad_set_id, anomalies)

        return {
            "ad_set_id": ad_set_id,
            "ad_set_name": ad_set.name,
            "monitoring_status": ad_set.monitoring_status.value,
            "current_metrics": {
                "ctr": current_metrics.ctr,
                "cpa": current_metrics.cpa,
                "frequency": current_metrics.frequency,
                "engagement_rate": current_metrics.engagement_rate,
                "impressions": current_metrics.impressions,
                "spend": current_metrics.spend,
            },
            "anomalies": anomalies,
            "should_alert": should_alert,
            "last_updated": current_metrics.date.isoformat(),
        }
