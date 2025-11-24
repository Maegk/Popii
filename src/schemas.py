"""
Pydantic schemas for API request/response validation
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# Ad Set Schemas
class AdSetCreate(BaseModel):
    external_id: str = Field(..., description="External ad set ID from platform")
    platform: str = Field(..., description="Ad platform (meta, google, etc)")
    name: str = Field(..., description="Ad set name")
    campaign_id: Optional[str] = None
    check_interval_minutes: int = Field(60, description="How often to check metrics")
    auto_rotation_enabled: bool = Field(True, description="Enable auto-rotation")


class AdSetResponse(BaseModel):
    id: int
    external_id: str
    platform: str
    name: str
    monitoring_status: str
    auto_rotation_enabled: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Metrics Schemas
class MetricsCreate(BaseModel):
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    spend: float = 0.0
    reach: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    negative_feedback: int = 0
    hide_clicks: int = 0
    report_clicks: int = 0


class MetricsResponse(BaseModel):
    ctr: float
    cpa: float
    cpm: float
    frequency: float
    engagement_rate: float
    impressions: int
    spend: float
    date: datetime

    class Config:
        from_attributes = True


# Fatigue Schemas
class FatigueStatusResponse(BaseModel):
    ad_set_id: int
    ad_set_name: str
    fatigue_score: float
    fatigue_level: str
    prediction_confidence: float
    current_metrics: Dict[str, Any]
    action_required: bool
    last_updated: datetime


class FatiguePredictionRequest(BaseModel):
    ad_set_id: int
    lookahead_days: Optional[int] = 3


class FatiguePredictionResponse(BaseModel):
    ad_set_id: int
    current_score: float
    predicted_score: float
    fatigue_level: str
    confidence: float
    lookahead_days: int
    features: Dict[str, float]
    action_required: bool


# Creative Schemas
class CreativeCreate(BaseModel):
    ad_set_id: int
    name: str
    format: str  # image, video, carousel, collection
    headline: Optional[str] = None
    body_text: Optional[str] = None
    call_to_action: Optional[str] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None


class CreativeResponse(BaseModel):
    id: int
    name: str
    format: str
    status: str
    headline: Optional[str]
    body_text: Optional[str]
    call_to_action: Optional[str]
    variation_type: str
    generated_by_ai: bool
    created_at: datetime

    class Config:
        from_attributes = True


class GenerateVariationsRequest(BaseModel):
    original_creative_id: int
    count: int = Field(5, ge=1, le=10, description="Number of variations (1-10)")
    variation_types: List[str] = Field(
        default=["hook", "angle", "copy"],
        description="Types of variations to generate",
    )
    audience_segment: Optional[str] = Field(
        None,
        description="Audience segment ID for personalization",
    )


class GenerateVariationsResponse(BaseModel):
    original_creative_id: int
    variations_count: int
    variations: List[CreativeResponse]


# Rotation Schemas
class RotationCheckResponse(BaseModel):
    ad_set_id: int
    rotation_needed: bool
    rotation_executed: bool = False
    fatigue_score: float
    fatigue_level: Optional[str] = None
    paused_creative_id: Optional[int] = None
    new_creative_id: Optional[int] = None
    reason: Optional[str] = None
    timestamp: Optional[str] = None


class RotationHistoryResponse(BaseModel):
    creative_id: int
    creative_name: str
    paused_at: str
    variation_type: str
    was_ai_generated: bool


# Learning Schemas
class AudienceInsightResponse(BaseModel):
    segment_id: str
    segment_name: str
    preferred_format: Optional[str]
    preferred_hook_type: Optional[str]
    preferred_tone: Optional[str]
    avg_ctr: float
    avg_cpa: float
    avg_engagement_rate: float
    confidence_score: float
    sample_size: int
    top_hooks: Optional[List[str]]
    top_ctas: Optional[List[Dict[str, Any]]]

    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    type: str
    recommendation: str
    reason: str
    confidence: float


# Monitoring Schemas
class MonitoringStatusResponse(BaseModel):
    ad_set_id: int
    ad_set_name: str
    monitoring_status: str
    current_metrics: Dict[str, Any]
    anomalies: Dict[str, Any]
    should_alert: bool
    last_updated: str


# Generic Response
class SuccessResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
