from pydantic import PostgresDsn, RedisDsn, SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # === Application Settings ===
    app_name: str = Field("LLMProductRecommender", alias="APP_NAME")
    app_env: str = Field("development", alias="APP_ENV")
    app_debug: bool = Field(True, alias="APP_DEBUG")
    api_version: str = Field("v1", alias="API_VERSION")
    host: str = Field("0.0.0.0", alias="HOST")
    port: int = Field(8000, alias="PORT")

    # === Database Settings ===
    db_host: str = Field(..., alias="DB_HOST")
    db_port: int = Field(..., alias="DB_PORT")
    db_user: str = Field(..., alias="DB_USER")
    db_password: SecretStr = Field(..., alias="DB_PASSWORD")
    db_name: str = Field(..., alias="DB_NAME")
    database_url: str = Field(..., alias="DATABASE_URL")

    # === JWT Authentication Settings ===
    secret_key: SecretStr = Field(..., alias="SECRET_KEY")
    algorithm: str = Field("HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    # === Redis Cache Settings ===
    redis_host: str = Field(..., alias="REDIS_HOST")
    redis_port: int = Field(..., alias="REDIS_PORT")
    redis_db: int = Field(..., alias="REDIS_DB")
    redis_url: RedisDsn | None = Field(None, alias="REDIS_URL")

    # === Hugging Face Transformers Settings ===
    hf_token: SecretStr | None = Field(None, alias="HF_TOKEN")
    hf_model_name: str = Field("sentence-transformers/all-MiniLM-L6-v2", alias="HF_MODEL_NAME")

    # === Feedback and Monitoring Settings ===
    enable_feedback_collection: bool = Field(True, alias="ENABLE_FEEDBACK_COLLECTION")
    log_level: str = Field("debug", alias="LOG_LEVEL")
    embedding_model_name: str = Field("sentence-transformers/all-MiniLM-L6-v2", alias="EMBEDDING_MODEL_NAME")
    top_k: int = Field(10, alias="TOP_K")

    # === Pydantic Settings Configuration ===
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

# Instantiate config
settings = Settings()