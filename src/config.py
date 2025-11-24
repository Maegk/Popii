"""
Application configuration
"""
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "Creative Fatigue Detection System"
    app_env: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/creative_fatigue"
    database_pool_size: int = 10
    database_max_overflow: int = 20

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_max_connections: int = 50

    # Celery
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # Meta (Facebook) Ads API
    meta_access_token: Optional[str] = None
    meta_ad_account_id: Optional[str] = None
    meta_app_id: Optional[str] = None
    meta_app_secret: Optional[str] = None
    meta_api_version: str = "v19.0"

    # Anthropic API
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-5-sonnet-20241022"

    # OpenAI API
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4-turbo-preview"

    # Creative Generation Settings
    creative_generator: str = "anthropic"  # Options: anthropic, openai
    creative_variations_per_request: int = 5
    creative_generation_timeout: int = 60

    # Fatigue Detection Thresholds
    fatigue_frequency_threshold: int = 6
    fatigue_ctr_drop_percent: float = 20.0
    fatigue_cpa_increase_percent: float = 25.0
    fatigue_engagement_drop_percent: float = 30.0
    min_impressions_for_analysis: int = 1000
    min_days_for_analysis: int = 3

    # Prediction Settings
    prediction_lookahead_days: int = 3
    prediction_confidence_threshold: float = 0.7
    prediction_model: str = "gradient_boosting"  # Options: gradient_boosting, random_forest, prophet

    # Monitoring Settings
    metrics_collection_interval_minutes: int = 60
    metrics_retention_days: int = 90
    enable_real_time_monitoring: bool = True

    # Auto-Rotation Settings
    enable_auto_rotation: bool = True
    auto_rotation_fatigue_threshold: float = 0.7
    auto_rotation_cooldown_hours: int = 24
    max_active_creatives_per_adset: int = 3

    # Learning Engine
    enable_learning_engine: bool = True
    learning_update_interval_hours: int = 6
    min_samples_for_learning: int = 100

    # Security
    secret_key: str = "change-me-in-production"
    api_key: Optional[str] = None
    allowed_origins: str = "http://localhost:3000,http://localhost:8000"

    # Monitoring & Observability
    sentry_dsn: Optional[str] = None
    enable_prometheus: bool = True
    prometheus_port: int = 9090

    # Rate Limiting
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000

    # Feature Flags
    enable_webhook_notifications: bool = False
    enable_slack_notifications: bool = False
    enable_email_notifications: bool = False

    # Slack
    slack_webhook_url: Optional[str] = None
    slack_channel: str = "#ad-performance"

    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    email_from: str = "noreply@yourcompany.com"

    def get_allowed_origins(self) -> list[str]:
        """Get list of allowed origins"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Global settings instance
settings = get_settings()
