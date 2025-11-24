"""
Creative Performance model
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, Float, ForeignKey, DateTime, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, TimestampMixin


class CreativePerformance(Base, TimestampMixin):
    """Creative Performance model for tracking individual creative performance"""

    __tablename__ = "creative_performance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    creative_id: Mapped[int] = mapped_column(Integer, ForeignKey("creatives.id"), nullable=False, index=True)

    # Time period
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    # Performance metrics
    impressions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    clicks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    conversions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    ctr: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    cpa: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    spend: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Engagement metrics
    engagement_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    video_watch_time_seconds: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Performance scores (calculated)
    performance_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    roi: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Audience insights for this creative
    audience_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relationships
    creative: Mapped["Creative"] = relationship("Creative", back_populates="performance_records")

    __table_args__ = (
        Index("idx_creative_date", "creative_id", "date"),
    )

    def __repr__(self) -> str:
        return (
            f"<CreativePerformance(creative_id={self.creative_id}, date={self.date}, "
            f"ctr={self.ctr:.2f}, performance_score={self.performance_score:.2f})>"
        )
