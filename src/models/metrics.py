"""
Metrics model
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, Float, ForeignKey, DateTime, BigInteger, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, TimestampMixin


class Metrics(Base, TimestampMixin):
    """Metrics model for tracking ad performance"""

    __tablename__ = "metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ad_set_id: Mapped[int] = mapped_column(Integer, ForeignKey("ad_sets.id"), nullable=False, index=True)

    # Time period
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    # Core metrics
    impressions: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    clicks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    conversions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Performance metrics
    ctr: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)  # Click-through rate (%)
    cpc: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)  # Cost per click
    cpa: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)  # Cost per acquisition
    cpm: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)  # Cost per mille (1000 impressions)

    # Engagement metrics
    likes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    comments: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    shares: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    engagement_rate: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Frequency metrics
    frequency: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    reach: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)

    # Cost metrics
    spend: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    # Negative signals
    negative_feedback: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    hide_clicks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    report_clicks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    ad_set: Mapped["AdSet"] = relationship("AdSet", back_populates="metrics")

    __table_args__ = (
        Index("idx_ad_set_date", "ad_set_id", "date"),
    )

    def __repr__(self) -> str:
        return (
            f"<Metrics(ad_set_id={self.ad_set_id}, date={self.date}, "
            f"ctr={self.ctr:.2f}, cpa={self.cpa:.2f}, frequency={self.frequency:.2f})>"
        )
