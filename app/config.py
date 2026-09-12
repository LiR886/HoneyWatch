from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "HoneyWatch"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = False

    database_url: str = "sqlite:////app/data/honeywatch.db"
    log_dir: str = "/app/logs"

    dashboard_username: str = "admin"
    dashboard_password: str = "change-me-now"

    trust_proxy_headers: bool = False

    brute_force_threshold: int = 5
    brute_force_window_seconds: int = 60
    username_spray_threshold: int = 5
    username_spray_window_seconds: int = 120
    rapid_request_threshold: int = 10
    rapid_request_window_seconds: int = 10
    alert_cooldown_seconds: int = 60

    high_value_usernames: str = "admin,administrator,root,sysadmin,support"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def high_value_username_set(self) -> set[str]:
        return {
            item.strip().lower()
            for item in self.high_value_usernames.split(",")
            if item.strip()
        }

    def ensure_directories(self) -> None:
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_directories()
    return settings
