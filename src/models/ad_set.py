"""
Ad Set model
"""
from typing import Optional

from sqlalchemy import String, Integer, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from src.models.base import Base, TimestampMixin


class AdPlatform(str, enum.Enum):
    """Ad platform types"""

    META = "meta"
    GOOGLE = "google"
    TIKTOK = "tiktok"
    LINKEDIN = "linkedin"


class MonitoringStatus(str, enum.Enum):
    """Monitoring status"""

    ACTIVE = "active"
    PAUSED = "paused"
    STOPPED = "stopped"


class AdSet(Base, TimestampMixin):
    """Ad Set model"""

    __tablename__ = "ad_sets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    platform: Mapped[AdPlatform] = mapped_column(SQLEnum(AdPlatform), nullable=False)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    campaign_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Monitoring settings
    monitoring_status: Mapped[MonitoringStatus] = mapped_column(
        SQLEnum(MonitoringStatus),
        default=MonitoringStatus.ACTIVE,
        nullable=False,
    )
    check_interval_minutes: Mapped[int] = mapped_column(Integer, default=60, nullable=False)

    # Auto-rotation settings
    auto_rotation_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    max_active_creatives: Mapped[int] = mapped_column(Integer, default=3, nullable=False)

    # Relationships
    metrics: Mapped[list["Metrics"]] = relationship(
        "Metrics",
        back_populates="ad_set",
        cascade="all, delete-orphan",
    )
    creatives: Mapped[list["Creative"]] = relationship(
        "Creative",
        back_populates="ad_set",
        cascade="all, delete-orphan",
    )
    fatigue_scores: Mapped[list["FatigueScore"]] = relationship(
        "FatigueScore",
        back_populates="ad_set",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<AdSet(id={self.id}, external_id='{self.external_id}', platform='{self.platform}')>"
