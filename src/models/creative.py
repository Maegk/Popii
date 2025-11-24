"""
Creative model
"""
from typing import Optional
import enum

from sqlalchemy import String, Integer, Text, Boolean, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, TimestampMixin


class CreativeFormat(str, enum.Enum):
    """Creative format types"""

    IMAGE = "image"
    VIDEO = "video"
    CAROUSEL = "carousel"
    COLLECTION = "collection"


class CreativeStatus(str, enum.Enum):
    """Creative status"""

    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"
    TESTING = "testing"


class CreativeVariationType(str, enum.Enum):
    """Creative variation type"""

    ORIGINAL = "original"
    HOOK_VARIATION = "hook_variation"
    ANGLE_VARIATION = "angle_variation"
    FORMAT_VARIATION = "format_variation"
    COPY_VARIATION = "copy_variation"
    COMBINATION = "combination"


class Creative(Base, TimestampMixin):
    """Creative model"""

    __tablename__ = "creatives"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True, index=True)
    ad_set_id: Mapped[int] = mapped_column(Integer, ForeignKey("ad_sets.id"), nullable=False, index=True)

    # Creative details
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    format: Mapped[CreativeFormat] = mapped_column(SQLEnum(CreativeFormat), nullable=False)
    status: Mapped[CreativeStatus] = mapped_column(
        SQLEnum(CreativeStatus),
        default=CreativeStatus.TESTING,
        nullable=False,
    )

    # Content
    headline: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    body_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    call_to_action: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    video_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    # Variation tracking
    variation_type: Mapped[CreativeVariationType] = mapped_column(
        SQLEnum(CreativeVariationType),
        default=CreativeVariationType.ORIGINAL,
        nullable=False,
    )
    parent_creative_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("creatives.id"),
        nullable=True,
    )

    # AI generation metadata
    generated_by_ai: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    generation_prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    generation_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relationships
    ad_set: Mapped["AdSet"] = relationship("AdSet", back_populates="creatives")
    parent_creative: Mapped[Optional["Creative"]] = relationship(
        "Creative",
        remote_side=[id],
        backref="variations",
    )
    performance_records: Mapped[list["CreativePerformance"]] = relationship(
        "CreativePerformance",
        back_populates="creative",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Creative(id={self.id}, name='{self.name}', format='{self.format}')>"
