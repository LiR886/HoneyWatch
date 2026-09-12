import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.config import get_settings


settings = get_settings()
security = HTTPBasic()


def require_dashboard_auth(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    username_ok = secrets.compare_digest(credentials.username, settings.dashboard_username)
    password_ok = secrets.compare_digest(credentials.password, settings.dashboard_password)

    if not (username_ok and password_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid dashboard credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username
