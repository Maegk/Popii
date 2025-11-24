"""
Basic usage example for Creative Fatigue Detection System

This example demonstrates:
1. Creating an ad set
2. Collecting metrics
3. Predicting fatigue
4. Generating creative variations
5. Auto-rotating creatives
"""
import asyncio
import httpx


BASE_URL = "http://localhost:8000"


async def main():
    """Main example flow"""
    async with httpx.AsyncClient() as client:
        print("=" * 80)
        print("Creative Fatigue Detection System - Basic Usage Example")
        print("=" * 80)
        print()

        # 1. Create an ad set to monitor
        print("1. Creating ad set...")
        ad_set_data = {
            "external_id": "meta_adset_123456",
            "platform": "meta",
            "name": "Summer Campaign - Conversion Ad Set",
            "campaign_id": "campaign_001",
            "check_interval_minutes": 60,
            "auto_rotation_enabled": True,
        }

        response = await client.post(f"{BASE_URL}/api/v1/ad-sets", json=ad_set_data)
        ad_set = response.json()
        ad_set_id = ad_set["id"]
        print(f"✓ Created ad set: ID={ad_set_id}, Name='{ad_set['name']}'")
        print()

        # 2. Create an original creative
        print("2. Creating original creative...")
        creative_data = {
            "ad_set_id": ad_set_id,
            "name": "Summer Sale Creative v1",
            "format": "image",
            "headline": "Get 50% Off Summer Collection",
            "body_text": "Limited time offer! Shop our summer collection and save big. "
            "Premium quality, unbeatable prices. Free shipping on orders over $50.",
            "call_to_action": "Shop Now",
            "image_url": "https://example.com/summer-sale.jpg",
        }

        response = await client.post(f"{BASE_URL}/api/v1/creative/create", json=creative_data)
        creative = response.json()
        creative_id = creative["id"]
        print(f"✓ Created creative: ID={creative_id}, Name='{creative['name']}'")
        print()

        # 3. Simulate metrics collection (in real scenario, this comes from ad platform)
        print("3. Collecting metrics (simulated)...")
        metrics_data = {
            "impressions": 10000,
            "clicks": 250,
            "conversions": 25,
            "spend": 500.00,
            "reach": 8000,
            "likes": 50,
            "comments": 10,
            "shares": 5,
            "negative_feedback": 2,
            "hide_clicks": 1,
            "report_clicks": 0,
        }

        response = await client.post(
            f"{BASE_URL}/api/v1/metrics/collect/{ad_set_id}",
            json=metrics_data,
        )
        result = response.json()
        print(f"✓ Collected metrics: CTR={result['data']['ctr']:.2f}%, "
              f"CPA=${result['data']['cpa']:.2f}, Frequency={result['data']['frequency']:.2f}")
        print()

        # 4. Get monitoring status
        print("4. Checking monitoring status...")
        response = await client.get(f"{BASE_URL}/api/v1/monitoring/status/{ad_set_id}")
        status = response.json()
        print(f"✓ Monitoring Status:")
        print(f"  - CTR: {status['current_metrics']['ctr']:.2f}%")
        print(f"  - CPA: ${status['current_metrics']['cpa']:.2f}")
        print(f"  - Frequency: {status['current_metrics']['frequency']:.2f}")
        print(f"  - Should Alert: {status['should_alert']}")
        print()

        # 5. Predict creative fatigue
        print("5. Predicting creative fatigue...")
        prediction_data = {
            "ad_set_id": ad_set_id,
            "lookahead_days": 3,
        }

        response = await client.post(
            f"{BASE_URL}/api/v1/fatigue/predict",
            json=prediction_data,
        )
        prediction = response.json()
        print(f"✓ Fatigue Prediction:")
        print(f"  - Current Score: {prediction['current_score']:.2f}")
        print(f"  - Predicted Score (3 days): {prediction['predicted_score']:.2f}")
        print(f"  - Fatigue Level: {prediction['fatigue_level']}")
        print(f"  - Confidence: {prediction['confidence']:.2f}")
        print(f"  - Action Required: {prediction['action_required']}")
        print()

        # 6. Generate creative variations using AI
        print("6. Generating creative variations with AI...")
        generation_data = {
            "original_creative_id": creative_id,
            "count": 3,
            "variation_types": ["hook", "angle", "copy"],
        }

        response = await client.post(
            f"{BASE_URL}/api/v1/creative/generate",
            json=generation_data,
        )
        variations = response.json()
        print(f"✓ Generated {variations['variations_count']} variations:")
        for i, var in enumerate(variations["variations"], 1):
            print(f"  {i}. {var['name']}")
            print(f"     - Headline: {var['headline']}")
            print(f"     - Variation Type: {var['variation_type']}")
        print()

        # 7. Get creative suggestions
        print("7. Getting AI-powered creative suggestions...")
        response = await client.get(f"{BASE_URL}/api/v1/creative/suggestions/{ad_set_id}")
        suggestions = response.json()
        print(f"✓ Creative Suggestions:")
        for sugg in suggestions["suggestions"]:
            print(f"  - [{sugg['priority'].upper()}] {sugg['type']}: {sugg['reason']}")
        print()

        # 8. Check rotation status
        print("8. Checking if creative rotation is needed...")
        response = await client.post(f"{BASE_URL}/api/v1/rotation/check/{ad_set_id}")
        rotation = response.json()
        print(f"✓ Rotation Status:")
        print(f"  - Rotation Needed: {rotation['rotation_needed']}")
        print(f"  - Rotation Executed: {rotation.get('rotation_executed', False)}")
        print(f"  - Fatigue Score: {rotation['fatigue_score']:.2f}")
        if rotation.get("reason"):
            print(f"  - Reason: {rotation['reason']}")
        print()

        # 9. Get recommendations
        print("9. Getting strategic recommendations...")
        response = await client.get(f"{BASE_URL}/api/v1/learning/recommendations/{ad_set_id}")
        recommendations = response.json()
        print(f"✓ Recommendations:")
        for rec in recommendations:
            print(f"  - [{rec['type'].upper()}] {rec['recommendation']}")
            print(f"    Reason: {rec['reason']} (Confidence: {rec['confidence']:.0%})")
        print()

        print("=" * 80)
        print("Example completed successfully!")
        print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
