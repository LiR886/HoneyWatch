from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Alert, LoginAttempt
from app.services.dashboard_auth import require_dashboard_auth


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def _stats(db: Session) -> dict:
    total_attempts = int(db.execute(select(func.count(LoginAttempt.id))).scalar_one())
    unique_ips = int(db.execute(select(func.count(func.distinct(LoginAttempt.source_ip)))).scalar_one())
    total_alerts = int(db.execute(select(func.count(Alert.id))).scalar_one())

    since = datetime.now(timezone.utc) - timedelta(hours=24)
    attempts_24h = int(
        db.execute(
            select(func.count(LoginAttempt.id)).where(LoginAttempt.created_at >= since)
        ).scalar_one()
    )

    top_usernames = db.execute(
        select(LoginAttempt.username, func.count(LoginAttempt.id).label("count"))
        .group_by(LoginAttempt.username)
        .order_by(desc("count"))
        .limit(8)
    ).all()

    top_ips = db.execute(
        select(LoginAttempt.source_ip, func.count(LoginAttempt.id).label("count"))
        .group_by(LoginAttempt.source_ip)
        .order_by(desc("count"))
        .limit(8)
    ).all()

    recent_attempts = db.execute(
        select(LoginAttempt).order_by(LoginAttempt.created_at.desc()).limit(20)
    ).scalars().all()

    recent_alerts = db.execute(
        select(Alert).order_by(Alert.created_at.desc()).limit(20)
    ).scalars().all()

    return {
        "total_attempts": total_attempts,
        "unique_ips": unique_ips,
        "total_alerts": total_alerts,
        "attempts_24h": attempts_24h,
        "top_usernames": [{"name": name or "(empty)", "count": count} for name, count in top_usernames],
        "top_ips": [{"ip": ip, "count": count} for ip, count in top_ips],
        "recent_attempts": recent_attempts,
        "recent_alerts": recent_alerts,
    }


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    _: str = Depends(require_dashboard_auth),
    db: Session = Depends(get_db),
):
    context = {"request": request, **_stats(db)}
    return templates.TemplateResponse(request=request, name="dashboard.html", context=context,)


@router.get("/api/stats")
def api_stats(
    _: str = Depends(require_dashboard_auth),
    db: Session = Depends(get_db),
):
    data = _stats(db)
    return {
        "total_attempts": data["total_attempts"],
        "unique_ips": data["unique_ips"],
        "total_alerts": data["total_alerts"],
        "attempts_24h": data["attempts_24h"],
        "top_usernames": data["top_usernames"],
        "top_ips": data["top_ips"],
    }
