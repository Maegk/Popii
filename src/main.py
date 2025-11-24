"""
Main FastAPI application
"""
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.config import settings
from src.database import get_db, init_db
from src.models.ad_set import AdSet, AdPlatform
from src.models.creative import Creative
from src.schemas import (
    AdSetCreate,
    AdSetResponse,
    MetricsCreate,
    FatigueStatusResponse,
    FatiguePredictionRequest,
    FatiguePredictionResponse,
    CreativeCreate,
    CreativeResponse,
    GenerateVariationsRequest,
    GenerateVariationsResponse,
    RotationCheckResponse,
    RotationHistoryResponse,
    AudienceInsightResponse,
    RecommendationResponse,
    MonitoringStatusResponse,
    SuccessResponse,
    ErrorResponse,
)
from src.core.monitoring import MetricsMonitor
from src.core.prediction import FatiguePredictor
from src.core.generation import CreativeGenerator
from src.core.rotation import CreativeRotator
from src.core.learning import LearningEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting Creative Fatigue Detection System...")
    await init_db()
    logger.info("Database initialized")
    yield
    # Shutdown
    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Automated Creative Fatigue Detection & Refresh System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "now"}


# ============================================================================
# AD SET ENDPOINTS
# ============================================================================


@app.post(
    "/api/v1/ad-sets",
    response_model=AdSetResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Ad Sets"],
)
async def create_ad_set(
    ad_set_data: AdSetCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new ad set to monitor"""
    try:
        ad_set = AdSet(
            external_id=ad_set_data.external_id,
            platform=AdPlatform(ad_set_data.platform),
            name=ad_set_data.name,
            campaign_id=ad_set_data.campaign_id,
            check_interval_minutes=ad_set_data.check_interval_minutes,
            auto_rotation_enabled=ad_set_data.auto_rotation_enabled,
        )

        db.add(ad_set)
        await db.commit()
        await db.refresh(ad_set)

        logger.info(f"Created ad set: {ad_set.id} - {ad_set.name}")
        return ad_set

    except Exception as e:
        logger.error(f"Error creating ad set: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get(
    "/api/v1/ad-sets/{ad_set_id}",
    response_model=AdSetResponse,
    tags=["Ad Sets"],
)
async def get_ad_set(
    ad_set_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get ad set by ID"""
    query = select(AdSet).where(AdSet.id == ad_set_id)
    result = await db.execute(query)
    ad_set = result.scalar_one_or_none()

    if not ad_set:
        raise HTTPException(status_code=404, detail="Ad set not found")

    return ad_set


@app.get(
    "/api/v1/ad-sets",
    response_model=List[AdSetResponse],
    tags=["Ad Sets"],
)
async def list_ad_sets(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """List all ad sets"""
    query = select(AdSet).offset(skip).limit(limit)
    result = await db.execute(query)
    return list(result.scalars().all())


# ============================================================================
# MONITORING ENDPOINTS
# ============================================================================


@app.post(
    "/api/v1/metrics/collect/{ad_set_id}",
    response_model=SuccessResponse,
    tags=["Monitoring"],
)
async def collect_metrics(
    ad_set_id: int,
    platform_data: dict,
    db: AsyncSession = Depends(get_db),
):
    """Collect and store metrics for an ad set"""
    try:
        monitor = MetricsMonitor(db)
        metrics = await monitor.collect_metrics(ad_set_id, platform_data)

        return SuccessResponse(
            success=True,
            message="Metrics collected successfully",
            data={
                "metrics_id": metrics.id,
                "ctr": metrics.ctr,
                "cpa": metrics.cpa,
                "frequency": metrics.frequency,
            },
        )
    except Exception as e:
        logger.error(f"Error collecting metrics: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get(
    "/api/v1/monitoring/status/{ad_set_id}",
    response_model=MonitoringStatusResponse,
    tags=["Monitoring"],
)
async def get_monitoring_status(
    ad_set_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get comprehensive monitoring status for an ad set"""
    monitor = MetricsMonitor(db)
    status_data = await monitor.get_monitoring_status(ad_set_id)

    if "error" in status_data:
        raise HTTPException(status_code=404, detail=status_data["error"])

    return status_data


# ============================================================================
# FATIGUE PREDICTION ENDPOINTS
# ============================================================================


@app.post(
    "/api/v1/fatigue/predict",
    response_model=FatiguePredictionResponse,
    tags=["Fatigue Detection"],
)
async def predict_fatigue(
    request: FatiguePredictionRequest,
    db: AsyncSession = Depends(get_db),
):
    """Predict creative fatigue for an ad set"""
    try:
        predictor = FatiguePredictor(db)
        score, level, details = await predictor.predict_fatigue(
            ad_set_id=request.ad_set_id,
            lookahead_days=request.lookahead_days,
        )

        return FatiguePredictionResponse(
            ad_set_id=request.ad_set_id,
            current_score=details.get("current_score", score),
            predicted_score=score,
            fatigue_level=level.value,
            confidence=details.get("confidence", 0.0),
            lookahead_days=details.get("lookahead_days", 3),
            features=details.get("features", {}),
            action_required=score >= settings.auto_rotation_fatigue_threshold,
        )
    except Exception as e:
        logger.error(f"Error predicting fatigue: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get(
    "/api/v1/fatigue/status/{ad_set_id}",
    tags=["Fatigue Detection"],
)
async def get_fatigue_status(
    ad_set_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get latest fatigue status for an ad set"""
    predictor = FatiguePredictor(db)
    latest = await predictor.get_latest_prediction(ad_set_id)

    if not latest:
        # Run prediction if none exists
        score, level, details = await predictor.predict_fatigue(ad_set_id)
        return {
            "ad_set_id": ad_set_id,
            "fatigue_score": score,
            "fatigue_level": level.value,
            "confidence": details.get("confidence", 0.0),
            "action_required": score >= settings.auto_rotation_fatigue_threshold,
        }

    return {
        "ad_set_id": ad_set_id,
        "fatigue_score": latest.score,
        "fatigue_level": latest.level.value,
        "confidence": latest.prediction_confidence,
        "action_required": latest.action_required,
        "predicted_at": latest.date.isoformat(),
    }


# ============================================================================
# CREATIVE GENERATION ENDPOINTS
# ============================================================================


@app.post(
    "/api/v1/creative/generate",
    response_model=GenerateVariationsResponse,
    tags=["Creative Generation"],
)
async def generate_creative_variations(
    request: GenerateVariationsRequest,
    db: AsyncSession = Depends(get_db),
):
    """Generate creative variations using AI"""
    try:
        generator = CreativeGenerator(db)
        variations = await generator.generate_variations(
            original_creative_id=request.original_creative_id,
            count=request.count,
            variation_types=request.variation_types,
            audience_segment=request.audience_segment,
        )

        return GenerateVariationsResponse(
            original_creative_id=request.original_creative_id,
            variations_count=len(variations),
            variations=[CreativeResponse.model_validate(v) for v in variations],
        )
    except Exception as e:
        logger.error(f"Error generating variations: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.post(
    "/api/v1/creative/create",
    response_model=CreativeResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Creative Generation"],
)
async def create_creative(
    creative_data: CreativeCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new creative"""
    try:
        from src.models.creative import CreativeFormat, CreativeStatus

        creative = Creative(
            ad_set_id=creative_data.ad_set_id,
            name=creative_data.name,
            format=CreativeFormat(creative_data.format),
            status=CreativeStatus.ACTIVE,
            headline=creative_data.headline,
            body_text=creative_data.body_text,
            call_to_action=creative_data.call_to_action,
            image_url=creative_data.image_url,
            video_url=creative_data.video_url,
        )

        db.add(creative)
        await db.commit()
        await db.refresh(creative)

        return creative
    except Exception as e:
        logger.error(f"Error creating creative: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get(
    "/api/v1/creative/suggestions/{ad_set_id}",
    tags=["Creative Generation"],
)
async def get_creative_suggestions(
    ad_set_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get AI-powered creative suggestions"""
    generator = CreativeGenerator(db)
    suggestions = await generator.get_creative_suggestions(ad_set_id)
    return {"ad_set_id": ad_set_id, "suggestions": suggestions}


# ============================================================================
# ROTATION ENDPOINTS
# ============================================================================


@app.post(
    "/api/v1/rotation/check/{ad_set_id}",
    response_model=RotationCheckResponse,
    tags=["Rotation"],
)
async def check_and_rotate(
    ad_set_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Check if rotation is needed and execute if necessary"""
    try:
        rotator = CreativeRotator(db)
        result = await rotator.check_and_rotate(ad_set_id)

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in rotation check: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get(
    "/api/v1/rotation/history/{ad_set_id}",
    response_model=List[RotationHistoryResponse],
    tags=["Rotation"],
)
async def get_rotation_history(
    ad_set_id: int,
    days: int = 30,
    db: AsyncSession = Depends(get_db),
):
    """Get rotation history for an ad set"""
    rotator = CreativeRotator(db)
    history = await rotator.get_rotation_history(ad_set_id, days)
    return history


# ============================================================================
# LEARNING ENGINE ENDPOINTS
# ============================================================================


@app.post(
    "/api/v1/learning/update-insights/{segment_id}",
    response_model=AudienceInsightResponse,
    tags=["Learning Engine"],
)
async def update_audience_insights(
    segment_id: str,
    segment_name: str,
    db: AsyncSession = Depends(get_db),
):
    """Update audience insights based on performance data"""
    try:
        engine = LearningEngine(db)
        insight = await engine.update_audience_insights(segment_id, segment_name)
        return insight
    except Exception as e:
        logger.error(f"Error updating insights: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get(
    "/api/v1/learning/recommendations/{ad_set_id}",
    response_model=List[RecommendationResponse],
    tags=["Learning Engine"],
)
async def get_recommendations(
    ad_set_id: int,
    audience_segment: str = None,
    db: AsyncSession = Depends(get_db),
):
    """Get AI-powered recommendations for creative strategy"""
    engine = LearningEngine(db)
    recommendations = await engine.get_recommendations(ad_set_id, audience_segment)
    return recommendations


# ============================================================================
# ERROR HANDLERS
# ============================================================================


@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Not found", "detail": str(exc)},
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"Internal error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
