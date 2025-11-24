"""
Audience Insight model
"""
from typing import Optional

from sqlalchemy import Integer, String, Float, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base, TimestampMixin


class AudienceInsight(Base, TimestampMixin):
    """Audience Insight model for learning engine"""

    __tablename__ = "audience_insights"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Audience segment
    segment_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    segment_name: Mapped[str] = mapped_column(String(500), nullable=False)
    segment_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Creative preferences
    preferred_format: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    preferred_hook_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    preferred_tone: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Performance patterns
    avg_ctr: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    avg_cpa: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    avg_engagement_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Fatigue patterns
    avg_fatigue_threshold_days: Mapped[float] = mapped_column(Float, default=7.0, nullable=False)
    frequency_tolerance: Mapped[float] = mapped_column(Float, default=6.0, nullable=False)

    # Learning metadata
    sample_size: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    last_updated_samples: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Top performing creative elements
    top_hooks: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    top_angles: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    top_ctas: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)

    __table_args__ = (
        Index("idx_segment_confidence", "segment_id", "confidence_score"),
    )

    def __repr__(self) -> str:
        return (
            f"<AudienceInsight(segment_id='{self.segment_id}', "
            f"confidence_score={self.confidence_score:.2f}, sample_size={self.sample_size})>"
        )
