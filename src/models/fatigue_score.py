"""
Fatigue Score model
"""
from datetime import datetime
from typing import Optional
import enum

from sqlalchemy import Integer, Float, ForeignKey, DateTime, String, Enum as SQLEnum, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, TimestampMixin


class FatigueLevel(str, enum.Enum):
    """Fatigue level categories"""

    LOW = "low"  # 0.0 - 0.3
    MODERATE = "moderate"  # 0.3 - 0.6
    HIGH = "high"  # 0.6 - 0.8
    CRITICAL = "critical"  # 0.8 - 1.0


class FatigueScore(Base, TimestampMixin):
    """Fatigue Score model for tracking creative fatigue"""

    __tablename__ = "fatigue_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ad_set_id: Mapped[int] = mapped_column(Integer, ForeignKey("ad_sets.id"), nullable=False, index=True)

    # Score details
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    score: Mapped[float] = mapped_column(Float, nullable=False)  # 0.0 - 1.0
    level: Mapped[FatigueLevel] = mapped_column(SQLEnum(FatigueLevel), nullable=False)

    # Contributing factors (weighted scores)
    frequency_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    ctr_decay_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    cpa_increase_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    engagement_drop_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    negative_feedback_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Prediction details
    is_prediction: Mapped[bool] = mapped_column(default=False, nullable=False)
    prediction_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    prediction_horizon_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Model metadata
    model_version: Mapped[str] = mapped_column(String(50), nullable=False)
    model_features: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Action tracking
    action_required: Mapped[bool] = mapped_column(default=False, nullable=False)
    action_taken: Mapped[bool] = mapped_column(default=False, nullable=False)
    action_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    ad_set: Mapped["AdSet"] = relationship("AdSet", back_populates="fatigue_scores")

    __table_args__ = (
        Index("idx_ad_set_date_fatigue", "ad_set_id", "date"),
        Index("idx_score_level", "score", "level"),
    )

    @classmethod
    def get_level_from_score(cls, score: float) -> FatigueLevel:
        """Get fatigue level from score"""
        if score < 0.3:
            return FatigueLevel.LOW
        elif score < 0.6:
            return FatigueLevel.MODERATE
        elif score < 0.8:
            return FatigueLevel.HIGH
        else:
            return FatigueLevel.CRITICAL

    def __repr__(self) -> str:
        return (
            f"<FatigueScore(ad_set_id={self.ad_set_id}, date={self.date}, "
            f"score={self.score:.2f}, level='{self.level}')>"
        )
