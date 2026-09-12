from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import LoginAttempt
from app.services.client_ip import get_client_ip
from app.services.detection import detect_for_attempt
from app.services.logging_service import event_logger


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"message": None},
    )


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"message": None},
    )


@router.post("/login", response_class=HTMLResponse)
def login_attempt(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    normalized_username = username.strip()[:255]
    source_ip = get_client_ip(request)
    user_agent = request.headers.get("user-agent", "")[:2000]

    attempt = LoginAttempt(
        source_ip=source_ip,
        username=normalized_username,
        password_provided=bool(password),
        password_length=len(password),
        user_agent=user_agent,
        endpoint="/login",
        method="POST",
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    event_logger.info(
        "event=LOGIN_ATTEMPT source_ip=%s username=%r password_provided=%s password_length=%s user_agent=%r",
        source_ip,
        normalized_username,
        bool(password),
        len(password),
        user_agent,
    )

    detect_for_attempt(db, attempt)

    return templates.TemplateResponse(request=request, name="login.html", context={
        "message": "Authentication failed. Please verify your credentials and try again."
    },
    status_code=401,
)
