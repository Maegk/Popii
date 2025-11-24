"""
Automated Creative Rotation System

Automatically rotates creatives based on fatigue predictions.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from loguru import logger

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.ad_set import AdSet
from src.models.creative import Creative, CreativeStatus
from src.models.fatigue_score import FatigueScore, FatigueLevel
from src.core.prediction import FatiguePredictor
from src.core.generation import CreativeGenerator
from src.config import settings


class CreativeRotator:
    """Handles automated creative rotation"""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.predictor = FatiguePredictor(db_session)
        self.generator = CreativeGenerator(db_session)

    async def check_and_rotate(self, ad_set_id: int) -> Dict[str, Any]:
        """
        Check if rotation is needed and execute if necessary

        Args:
            ad_set_id: Ad set ID to check

        Returns:
            Dict with rotation results
        """
        # Get ad set
        query = select(AdSet).where(AdSet.id == ad_set_id)
        result = await self.db.execute(query)
        ad_set = result.scalar_one_or_none()

        if not ad_set:
            return {"error": "Ad set not found"}

        # Check if auto-rotation is enabled
        if not ad_set.auto_rotation_enabled or not settings.enable_auto_rotation:
            return {
                "ad_set_id": ad_set_id,
                "rotation_needed": False,
                "reason": "Auto-rotation disabled",
            }

        # Get latest fatigue prediction
        fatigue_score_obj = await self.predictor.get_latest_prediction(ad_set_id)

        if not fatigue_score_obj:
            # No prediction yet - run prediction
            score, level, details = await self.predictor.predict_fatigue(ad_set_id)
        else:
            score = fatigue_score_obj.score
            level = fatigue_score_obj.level

        # Check if rotation is needed
        rotation_needed = (
            score >= settings.auto_rotation_fatigue_threshold
            or level in [FatigueLevel.HIGH, FatigueLevel.CRITICAL]
        )

        if not rotation_needed:
            return {
                "ad_set_id": ad_set_id,
                "rotation_needed": False,
                "fatigue_score": score,
                "fatigue_level": level.value,
                "reason": "Fatigue score below threshold",
            }

        # Check cooldown period
        if await self._is_in_cooldown(ad_set_id):
            return {
                "ad_set_id": ad_set_id,
                "rotation_needed": True,
                "rotation_executed": False,
                "reason": "In cooldown period",
                "fatigue_score": score,
            }

        # Execute rotation
        rotation_result = await self._execute_rotation(ad_set_id)

        return {
            "ad_set_id": ad_set_id,
            "rotation_needed": True,
            "rotation_executed": True,
            "fatigue_score": score,
            "fatigue_level": level.value,
            **rotation_result,
        }

    async def _execute_rotation(self, ad_set_id: int) -> Dict[str, Any]:
        """Execute creative rotation"""
        logger.info(f"Executing creative rotation for ad_set_id={ad_set_id}")

        # Get current active creatives
        active_creatives = await self._get_active_creatives(ad_set_id)

        if not active_creatives:
            return {
                "error": "No active creatives to rotate from",
                "action": "manual_intervention_needed",
            }

        # Select creative to rotate out (highest fatigue or oldest)
        creative_to_pause = await self._select_creative_to_rotate_out(active_creatives)

        # Check if we have variations ready
        available_variations = await self._get_available_variations(ad_set_id)

        new_creative = None
        if available_variations:
            # Use existing variation
            new_creative = available_variations[0]
            new_creative.status = CreativeStatus.ACTIVE
        else:
            # Generate new variations
            logger.info(f"No variations available, generating new ones...")
            try:
                variations = await self.generator.generate_variations(
                    original_creative_id=creative_to_pause.id,
                    count=settings.creative_variations_per_request,
                    variation_types=["hook", "angle", "copy"],
                )
                if variations:
                    new_creative = variations[0]
                    new_creative.status = CreativeStatus.ACTIVE
            except Exception as e:
                logger.error(f"Error generating variations: {e}")
                return {"error": f"Failed to generate variations: {e}"}

        # Pause old creative
        creative_to_pause.status = CreativeStatus.PAUSED

        await self.db.commit()

        logger.info(
            f"Rotation complete: Paused creative_id={creative_to_pause.id}, "
            f"Activated creative_id={new_creative.id if new_creative else None}"
        )

        return {
            "paused_creative_id": creative_to_pause.id,
            "paused_creative_name": creative_to_pause.name,
            "new_creative_id": new_creative.id if new_creative else None,
            "new_creative_name": new_creative.name if new_creative else None,
            "generated_new": not available_variations,
            "timestamp": datetime.now().isoformat(),
        }

    async def _get_active_creatives(self, ad_set_id: int) -> List[Creative]:
        """Get all active creatives for an ad set"""
        query = (
            select(Creative)
            .where(
                and_(
                    Creative.ad_set_id == ad_set_id,
                    Creative.status == CreativeStatus.ACTIVE,
                )
            )
            .order_by(Creative.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def _get_available_variations(self, ad_set_id: int) -> List[Creative]:
        """Get available variations ready to be activated"""
        query = (
            select(Creative)
            .where(
                and_(
                    Creative.ad_set_id == ad_set_id,
                    Creative.status == CreativeStatus.TESTING,
                    Creative.generated_by_ai == True,
                )
            )
            .order_by(Creative.created_at.desc())
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def _select_creative_to_rotate_out(
        self,
        active_creatives: List[Creative],
    ) -> Creative:
        """
        Select which creative to rotate out

        Prioritizes:
        1. Oldest creatives first
        2. Lowest performing (if performance data available)
        """
        # For now, select oldest
        # TODO: Incorporate performance data
        return min(active_creatives, key=lambda c: c.created_at)

    async def _is_in_cooldown(self, ad_set_id: int) -> bool:
        """Check if ad set is in cooldown period after last rotation"""
        # Get last rotation (last creative status change to PAUSED)
        query = (
            select(Creative)
            .where(
                and_(
                    Creative.ad_set_id == ad_set_id,
                    Creative.status == CreativeStatus.PAUSED,
                )
            )
            .order_by(Creative.updated_at.desc())
            .limit(1)
        )
        result = await self.db.execute(query)
        last_paused = result.scalar_one_or_none()

        if not last_paused:
            return False

        # Check if cooldown period has passed
        cooldown_threshold = datetime.now() - timedelta(
            hours=settings.auto_rotation_cooldown_hours
        )

        return last_paused.updated_at > cooldown_threshold

    async def schedule_rotation(
        self,
        ad_set_id: int,
        scheduled_time: datetime,
    ) -> Dict[str, Any]:
        """
        Schedule a future rotation

        Args:
            ad_set_id: Ad set ID
            scheduled_time: When to execute rotation

        Returns:
            Schedule confirmation
        """
        # In production, this would create a scheduled task
        # For now, return confirmation
        return {
            "ad_set_id": ad_set_id,
            "scheduled_time": scheduled_time.isoformat(),
            "status": "scheduled",
            "message": "Rotation scheduled successfully",
        }

    async def get_rotation_history(
        self,
        ad_set_id: int,
        days: int = 30,
    ) -> List[Dict[str, Any]]:
        """Get rotation history for an ad set"""
        start_date = datetime.now() - timedelta(days=days)

        # Get all paused creatives (rotations)
        query = (
            select(Creative)
            .where(
                and_(
                    Creative.ad_set_id == ad_set_id,
                    Creative.status == CreativeStatus.PAUSED,
                    Creative.updated_at >= start_date,
                )
            )
            .order_by(Creative.updated_at.desc())
        )
        result = await self.db.execute(query)
        paused_creatives = list(result.scalars().all())

        history = []
        for creative in paused_creatives:
            history.append(
                {
                    "creative_id": creative.id,
                    "creative_name": creative.name,
                    "paused_at": creative.updated_at.isoformat(),
                    "variation_type": creative.variation_type.value,
                    "was_ai_generated": creative.generated_by_ai,
                }
            )

        return history
