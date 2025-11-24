"""
AI-Powered Creative Generation System

Generates creative variations using AI (Claude/GPT).
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from loguru import logger

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.creative import Creative, CreativeFormat, CreativeVariationType, CreativeStatus
from src.models.ad_set import AdSet
from src.models.audience_insight import AudienceInsight
from src.config import settings


class CreativeGenerator:
    """Generates creative variations using AI"""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

        # Initialize AI clients
        if settings.creative_generator == "anthropic" and settings.anthropic_api_key:
            self.anthropic_client = AsyncAnthropic(api_key=settings.anthropic_api_key)
        else:
            self.anthropic_client = None

        if settings.openai_api_key:
            self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
        else:
            self.openai_client = None

    async def generate_variations(
        self,
        original_creative_id: int,
        count: int = 5,
        variation_types: Optional[List[str]] = None,
        audience_segment: Optional[str] = None,
    ) -> List[Creative]:
        """
        Generate creative variations using AI

        Args:
            original_creative_id: ID of original creative to vary
            count: Number of variations to generate
            variation_types: Types of variations (hook, angle, format, copy)
            audience_segment: Optional audience segment for personalization

        Returns:
            List of generated Creative objects
        """
        # Get original creative
        query = select(Creative).where(Creative.id == original_creative_id)
        result = await self.db.execute(query)
        original = result.scalar_one_or_none()

        if not original:
            raise ValueError(f"Creative {original_creative_id} not found")

        # Default variation types
        if not variation_types:
            variation_types = ["hook", "angle", "copy"]

        # Get audience insights if available
        audience_insights = None
        if audience_segment:
            audience_insights = await self._get_audience_insights(audience_segment)

        # Generate variations
        variations = []
        for i in range(count):
            variation_type = variation_types[i % len(variation_types)]

            # Generate content using AI
            generated_content = await self._generate_content(
                original=original,
                variation_type=variation_type,
                audience_insights=audience_insights,
            )

            # Create new creative
            new_creative = Creative(
                ad_set_id=original.ad_set_id,
                name=f"{original.name} - {variation_type.title()} Variation {i + 1}",
                format=original.format,
                status=CreativeStatus.TESTING,
                headline=generated_content.get("headline"),
                body_text=generated_content.get("body_text"),
                call_to_action=generated_content.get("call_to_action"),
                image_url=original.image_url,  # Copy from original
                video_url=original.video_url,  # Copy from original
                variation_type=self._map_variation_type(variation_type),
                parent_creative_id=original.id,
                generated_by_ai=True,
                generation_prompt=generated_content.get("prompt"),
                generation_metadata={
                    "model": settings.creative_generator,
                    "variation_type": variation_type,
                    "audience_segment": audience_segment,
                    "generated_at": datetime.now().isoformat(),
                },
            )

            self.db.add(new_creative)
            variations.append(new_creative)

        await self.db.commit()

        logger.info(
            f"Generated {len(variations)} variations for creative_id={original_creative_id}"
        )

        return variations

    async def _generate_content(
        self,
        original: Creative,
        variation_type: str,
        audience_insights: Optional[AudienceInsight] = None,
    ) -> Dict[str, Any]:
        """Generate creative content using AI"""
        # Build prompt
        prompt = self._build_generation_prompt(
            original=original,
            variation_type=variation_type,
            audience_insights=audience_insights,
        )

        # Generate using selected AI
        if settings.creative_generator == "anthropic" and self.anthropic_client:
            content = await self._generate_with_anthropic(prompt)
        elif self.openai_client:
            content = await self._generate_with_openai(prompt)
        else:
            # Fallback to template-based generation
            content = self._generate_with_template(original, variation_type)

        content["prompt"] = prompt
        return content

    def _build_generation_prompt(
        self,
        original: Creative,
        variation_type: str,
        audience_insights: Optional[AudienceInsight] = None,
    ) -> str:
        """Build prompt for AI generation"""
        prompt_parts = [
            "You are an expert ad copywriter specializing in high-converting social media ads.",
            "",
            "Original Creative:",
            f"Headline: {original.headline}",
            f"Body Text: {original.body_text}",
            f"CTA: {original.call_to_action}",
            f"Format: {original.format.value}",
            "",
        ]

        # Add audience insights
        if audience_insights:
            prompt_parts.extend(
                [
                    "Audience Insights:",
                    f"Segment: {audience_insights.segment_name}",
                    f"Preferred Format: {audience_insights.preferred_format}",
                    f"Preferred Hook: {audience_insights.preferred_hook_type}",
                    f"Preferred Tone: {audience_insights.preferred_tone}",
                    "",
                ]
            )

        # Add variation-specific instructions
        if variation_type == "hook":
            prompt_parts.extend(
                [
                    "Task: Generate a NEW HOOK variation.",
                    "- Create a completely different opening/headline that grabs attention",
                    "- Keep the core value proposition the same",
                    "- Try different hook types: question, stat, problem-solution, story",
                    "- Keep body text similar to original",
                ]
            )
        elif variation_type == "angle":
            prompt_parts.extend(
                [
                    "Task: Generate a NEW ANGLE variation.",
                    "- Approach the same product/service from a different angle",
                    "- Highlight different benefits or pain points",
                    "- Adjust both headline and body text",
                    "- Keep the tone consistent with the brand",
                ]
            )
        elif variation_type == "copy":
            prompt_parts.extend(
                [
                    "Task: Generate a COPY variation.",
                    "- Rewrite the body text with different wording",
                    "- Keep the same message but fresher phrasing",
                    "- Vary sentence structure and length",
                    "- Maintain the same hook/headline",
                ]
            )
        elif variation_type == "format":
            prompt_parts.extend(
                [
                    "Task: Generate a FORMAT variation.",
                    "- Adapt the creative for a different ad format",
                    "- Adjust copy length and structure for the new format",
                    "- Keep core message and value prop",
                ]
            )

        prompt_parts.extend(
            [
                "",
                "Output format (JSON):",
                "{",
                '  "headline": "...",',
                '  "body_text": "...",',
                '  "call_to_action": "..."',
                "}",
                "",
                "Generate the creative variation now:",
            ]
        )

        return "\n".join(prompt_parts)

    async def _generate_with_anthropic(self, prompt: str) -> Dict[str, Any]:
        """Generate content using Anthropic Claude"""
        try:
            message = await self.anthropic_client.messages.create(
                model=settings.anthropic_model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )

            # Parse response
            content_text = message.content[0].text

            # Try to extract JSON
            try:
                # Look for JSON in response
                start_idx = content_text.find("{")
                end_idx = content_text.rfind("}") + 1
                if start_idx != -1 and end_idx > start_idx:
                    json_str = content_text[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    raise ValueError("No JSON found in response")
            except (json.JSONDecodeError, ValueError):
                # Fallback: parse manually
                return {
                    "headline": content_text[:100],  # Use first part as headline
                    "body_text": content_text,
                    "call_to_action": "Learn More",
                }

        except Exception as e:
            logger.error(f"Error generating with Anthropic: {e}")
            return {
                "headline": "Error generating content",
                "body_text": str(e),
                "call_to_action": "Learn More",
            }

    async def _generate_with_openai(self, prompt: str) -> Dict[str, Any]:
        """Generate content using OpenAI GPT"""
        try:
            response = await self.openai_client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert ad copywriter. Respond only with valid JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
            )

            content_text = response.choices[0].message.content
            return json.loads(content_text)

        except Exception as e:
            logger.error(f"Error generating with OpenAI: {e}")
            return {
                "headline": "Error generating content",
                "body_text": str(e),
                "call_to_action": "Learn More",
            }

    def _generate_with_template(
        self,
        original: Creative,
        variation_type: str,
    ) -> Dict[str, Any]:
        """Fallback template-based generation"""
        templates = {
            "hook": [
                f"Discover: {original.headline}",
                f"What if {original.headline.lower()}?",
                f"The truth about {original.headline.lower()}",
            ],
            "angle": [
                original.body_text.replace("you", "your team")
                if original.body_text
                else "",
            ],
        }

        return {
            "headline": templates.get(variation_type, [original.headline])[0],
            "body_text": original.body_text,
            "call_to_action": original.call_to_action,
        }

    def _map_variation_type(self, variation_type: str) -> CreativeVariationType:
        """Map string variation type to enum"""
        mapping = {
            "hook": CreativeVariationType.HOOK_VARIATION,
            "angle": CreativeVariationType.ANGLE_VARIATION,
            "format": CreativeVariationType.FORMAT_VARIATION,
            "copy": CreativeVariationType.COPY_VARIATION,
        }
        return mapping.get(variation_type, CreativeVariationType.COMBINATION)

    async def _get_audience_insights(
        self,
        segment_id: str,
    ) -> Optional[AudienceInsight]:
        """Get audience insights for personalization"""
        query = select(AudienceInsight).where(AudienceInsight.segment_id == segment_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_creative_suggestions(
        self,
        ad_set_id: int,
    ) -> List[Dict[str, Any]]:
        """
        Get AI-powered creative suggestions for an ad set

        Analyzes performance and suggests what types of creatives to generate
        """
        # Get ad set
        query = select(AdSet).where(AdSet.id == ad_set_id)
        result = await self.db.execute(query)
        ad_set = result.scalar_one_or_none()

        if not ad_set:
            return []

        # Get existing creatives
        creatives_query = select(Creative).where(Creative.ad_set_id == ad_set_id)
        result = await self.db.execute(creatives_query)
        existing_creatives = list(result.scalars().all())

        # Analyze what's missing
        existing_formats = {c.format for c in existing_creatives}
        existing_variation_types = {c.variation_type for c in existing_creatives}

        suggestions = []

        # Suggest missing formats
        all_formats = {CreativeFormat.IMAGE, CreativeFormat.VIDEO, CreativeFormat.CAROUSEL}
        missing_formats = all_formats - existing_formats

        for fmt in missing_formats:
            suggestions.append(
                {
                    "type": "format_variation",
                    "format": fmt.value,
                    "reason": f"No {fmt.value} ads yet. This format could reach different audience segments.",
                    "priority": "high",
                }
            )

        # Suggest missing variation types
        if CreativeVariationType.HOOK_VARIATION not in existing_variation_types:
            suggestions.append(
                {
                    "type": "hook_variation",
                    "reason": "Try different hooks to capture attention in crowded feeds.",
                    "priority": "medium",
                }
            )

        return suggestions
