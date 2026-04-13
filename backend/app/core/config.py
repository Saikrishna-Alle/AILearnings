import os


class Settings:
    app_name: str = "AI Skill Platform"
    api_v1_prefix: str = "/api/v1"
    environment: str = "dev"
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg://root:root@localhost:5432/ail")
    auth_secret: str = os.getenv("AUTH_SECRET", "change-me-in-prod")


settings = Settings()
