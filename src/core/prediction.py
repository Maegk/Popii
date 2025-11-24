"""
Predictive Fatigue Detection System

Uses ML to predict creative fatigue BEFORE performance drops.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple
import numpy as np
from loguru import logger

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.ad_set import AdSet
from src.models.metrics import Metrics
from src.models.fatigue_score import FatigueScore, FatigueLevel
from src.config import settings


class FatiguePredictor:
    """Predicts creative fatigue using machine learning"""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.scaler = StandardScaler()
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        """Initialize the prediction model"""
        if settings.prediction_model == "gradient_boosting":
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42,
            )
        else:  # random_forest
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
            )

    async def predict_fatigue(
        self,
        ad_set_id: int,
        lookahead_days: Optional[int] = None,
    ) -> Tuple[float, FatigueLevel, Dict[str, Any]]:
        """
        Predict fatigue score for an ad set

        Args:
            ad_set_id: Ad set ID
            lookahead_days: Days ahead to predict (default from settings)

        Returns:
            Tuple of (score, level, details)
        """
        lookahead_days = lookahead_days or settings.prediction_lookahead_days

        # Get historical metrics
        metrics_history = await self._get_metrics_history(ad_set_id, days=30)

        if len(metrics_history) < settings.min_days_for_analysis:
            # Not enough data - use rule-based approach
            return await self._rule_based_prediction(ad_set_id)

        # Extract features
        features = self._extract_features(metrics_history)

        # Calculate current fatigue score
        current_score = self._calculate_fatigue_score(features)

        # Predict future fatigue
        predicted_score = self._predict_future_score(
            features,
            current_score,
            lookahead_days,
        )

        # Get fatigue level
        level = FatigueScore.get_level_from_score(predicted_score)

        # Build details
        details = {
            "current_score": current_score,
            "predicted_score": predicted_score,
            "lookahead_days": lookahead_days,
            "features": features,
            "confidence": self._calculate_confidence(metrics_history),
            "model_version": f"{settings.prediction_model}_v1.0",
        }

        # Store prediction
        await self._store_prediction(
            ad_set_id,
            predicted_score,
            level,
            details,
        )

        logger.info(
            f"Predicted fatigue for ad_set_id={ad_set_id}: "
            f"score={predicted_score:.2f}, level={level.value}"
        )

        return predicted_score, level, details

    def _extract_features(self, metrics_history: List[Metrics]) -> Dict[str, float]:
        """Extract ML features from metrics history"""
        if not metrics_history:
            return {}

        # Convert to arrays for easier computation
        ctrs = np.array([m.ctr for m in metrics_history])
        cpas = np.array([m.cpa for m in metrics_history if m.cpa > 0])
        frequencies = np.array([m.frequency for m in metrics_history])
        engagement_rates = np.array([m.engagement_rate for m in metrics_history])
        negative_feedback = np.array([m.negative_feedback for m in metrics_history])

        # Current values
        latest = metrics_history[0]  # Most recent

        # Trend calculations (simple linear regression slope)
        def calculate_trend(values):
            if len(values) < 2:
                return 0.0
            x = np.arange(len(values))
            return np.polyfit(x, values, 1)[0] if len(values) > 0 else 0.0

        ctr_trend = calculate_trend(ctrs)
        cpa_trend = calculate_trend(cpas) if len(cpas) > 0 else 0.0
        frequency_trend = calculate_trend(frequencies)
        engagement_trend = calculate_trend(engagement_rates)

        # Volatility (standard deviation)
        ctr_volatility = float(np.std(ctrs)) if len(ctrs) > 0 else 0.0
        cpa_volatility = float(np.std(cpas)) if len(cpas) > 0 else 0.0

        features = {
            # Current values
            "current_frequency": float(latest.frequency),
            "current_ctr": float(latest.ctr),
            "current_cpa": float(latest.cpa),
            "current_engagement_rate": float(latest.engagement_rate),
            "current_negative_feedback": float(latest.negative_feedback),
            # Averages
            "avg_frequency": float(np.mean(frequencies)),
            "avg_ctr": float(np.mean(ctrs)),
            "avg_cpa": float(np.mean(cpas)) if len(cpas) > 0 else 0.0,
            "avg_engagement": float(np.mean(engagement_rates)),
            # Trends
            "ctr_trend": float(ctr_trend),
            "cpa_trend": float(cpa_trend),
            "frequency_trend": float(frequency_trend),
            "engagement_trend": float(engagement_trend),
            # Volatility
            "ctr_volatility": ctr_volatility,
            "cpa_volatility": cpa_volatility,
            # Time-based
            "days_running": len(metrics_history),
        }

        return features

    def _calculate_fatigue_score(self, features: Dict[str, float]) -> float:
        """
        Calculate current fatigue score from features

        Score components:
        - Frequency score (0-1): Based on how many times users see the ad
        - CTR decay score (0-1): Based on CTR trend
        - CPA increase score (0-1): Based on CPA trend
        - Engagement drop score (0-1): Based on engagement trend
        - Negative feedback score (0-1): Based on negative signals
        """
        if not features:
            return 0.0

        # Frequency score (normalized to 0-1, threshold at 6)
        frequency_score = min(
            features.get("current_frequency", 0) / settings.fatigue_frequency_threshold,
            1.0,
        )

        # CTR decay score (negative trend is bad)
        ctr_trend = features.get("ctr_trend", 0)
        ctr_decay_score = max(0, -ctr_trend / 2.0)  # Normalize negative trend
        ctr_decay_score = min(ctr_decay_score, 1.0)

        # CPA increase score (positive trend is bad)
        cpa_trend = features.get("cpa_trend", 0)
        cpa_increase_score = max(0, cpa_trend / 5.0)  # Normalize positive trend
        cpa_increase_score = min(cpa_increase_score, 1.0)

        # Engagement drop score (negative trend is bad)
        engagement_trend = features.get("engagement_trend", 0)
        engagement_drop_score = max(0, -engagement_trend / 2.0)
        engagement_drop_score = min(engagement_drop_score, 1.0)

        # Negative feedback score
        negative_feedback = features.get("current_negative_feedback", 0)
        negative_feedback_score = min(negative_feedback / 10.0, 1.0)  # Normalize

        # Weighted combination
        weights = {
            "frequency": 0.3,
            "ctr_decay": 0.25,
            "cpa_increase": 0.25,
            "engagement_drop": 0.15,
            "negative_feedback": 0.05,
        }

        fatigue_score = (
            weights["frequency"] * frequency_score
            + weights["ctr_decay"] * ctr_decay_score
            + weights["cpa_increase"] * cpa_increase_score
            + weights["engagement_drop"] * engagement_drop_score
            + weights["negative_feedback"] * negative_feedback_score
        )

        return min(fatigue_score, 1.0)  # Cap at 1.0

    def _predict_future_score(
        self,
        features: Dict[str, float],
        current_score: float,
        lookahead_days: int,
    ) -> float:
        """
        Predict future fatigue score

        Uses current trends to project future score
        """
        # Simple projection based on trends
        frequency_trend = features.get("frequency_trend", 0)
        ctr_trend = features.get("ctr_trend", 0)
        engagement_trend = features.get("engagement_trend", 0)

        # Project trends forward
        frequency_projection = frequency_trend * lookahead_days
        ctr_projection = ctr_trend * lookahead_days
        engagement_projection = engagement_trend * lookahead_days

        # Adjust score based on projections
        score_adjustment = 0.0

        # If frequency is increasing, fatigue increases
        if frequency_projection > 0:
            score_adjustment += 0.1 * (frequency_projection / 2.0)

        # If CTR is decreasing, fatigue increases
        if ctr_projection < 0:
            score_adjustment += 0.15

        # If engagement is decreasing, fatigue increases
        if engagement_projection < 0:
            score_adjustment += 0.1

        predicted_score = current_score + score_adjustment

        # Natural fatigue increase over time (even with stable metrics)
        days_factor = lookahead_days / 7.0  # Normalize to weeks
        natural_increase = 0.05 * days_factor

        predicted_score += natural_increase

        return min(predicted_score, 1.0)  # Cap at 1.0

    async def _rule_based_prediction(
        self,
        ad_set_id: int,
    ) -> Tuple[float, FatigueLevel, Dict[str, Any]]:
        """
        Fallback rule-based prediction when insufficient data

        Uses simple thresholds instead of ML
        """
        # Get most recent metrics
        query = (
            select(Metrics)
            .where(Metrics.ad_set_id == ad_set_id)
            .order_by(Metrics.date.desc())
            .limit(1)
        )
        result = await self.db.execute(query)
        latest_metrics = result.scalar_one_or_none()

        if not latest_metrics:
            return 0.0, FatigueLevel.LOW, {"insufficient_data": True}

        # Simple rule-based score
        score = 0.0

        # Check frequency
        if latest_metrics.frequency >= settings.fatigue_frequency_threshold:
            score += 0.4

        # Check for performance issues (compared to typical values)
        if latest_metrics.ctr < 1.0:  # CTR below 1%
            score += 0.2

        if latest_metrics.negative_feedback > 5:
            score += 0.2

        level = FatigueScore.get_level_from_score(score)

        details = {
            "method": "rule_based",
            "reason": "insufficient_historical_data",
            "current_frequency": latest_metrics.frequency,
            "current_ctr": latest_metrics.ctr,
        }

        return score, level, details

    def _calculate_confidence(self, metrics_history: List[Metrics]) -> float:
        """Calculate prediction confidence based on data quality"""
        if not metrics_history:
            return 0.0

        # Factors affecting confidence:
        # 1. Amount of data
        data_points = len(metrics_history)
        data_score = min(data_points / 30.0, 1.0)  # 30 days = full confidence

        # 2. Data completeness (all metrics present)
        completeness = sum(
            1
            for m in metrics_history
            if m.impressions >= settings.min_impressions_for_analysis
        ) / len(metrics_history)

        # 3. Data consistency (low volatility in key metrics)
        ctrs = [m.ctr for m in metrics_history]
        ctr_volatility = np.std(ctrs) if len(ctrs) > 0 else 1.0
        consistency_score = max(0, 1.0 - (ctr_volatility / 10.0))  # Normalize

        confidence = (data_score * 0.5 + completeness * 0.3 + consistency_score * 0.2)

        return min(confidence, 1.0)

    async def _get_metrics_history(
        self,
        ad_set_id: int,
        days: int,
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

    async def _store_prediction(
        self,
        ad_set_id: int,
        score: float,
        level: FatigueLevel,
        details: Dict[str, Any],
    ) -> FatigueScore:
        """Store fatigue prediction in database"""
        fatigue_score = FatigueScore(
            ad_set_id=ad_set_id,
            date=datetime.now(),
            score=score,
            level=level,
            frequency_score=details["features"].get("current_frequency", 0) / 10.0,
            ctr_decay_score=max(0, -details["features"].get("ctr_trend", 0)),
            cpa_increase_score=max(0, details["features"].get("cpa_trend", 0)),
            engagement_drop_score=max(0, -details["features"].get("engagement_trend", 0)),
            negative_feedback_score=details["features"].get("current_negative_feedback", 0) / 10.0,
            is_prediction=True,
            prediction_confidence=details.get("confidence", 0.0),
            prediction_horizon_days=details.get("lookahead_days", 3),
            model_version=details.get("model_version", "v1.0"),
            model_features=details.get("features"),
            action_required=score >= settings.auto_rotation_fatigue_threshold,
        )

        self.db.add(fatigue_score)
        await self.db.commit()
        await self.db.refresh(fatigue_score)

        return fatigue_score

    async def get_latest_prediction(self, ad_set_id: int) -> Optional[FatigueScore]:
        """Get the most recent fatigue prediction"""
        query = (
            select(FatigueScore)
            .where(FatigueScore.ad_set_id == ad_set_id)
            .where(FatigueScore.is_prediction == True)
            .order_by(FatigueScore.date.desc())
            .limit(1)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
