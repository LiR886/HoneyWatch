from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Alert, LoginAttempt
from app.services.logging_service import alert_logger


settings = get_settings()


@dataclass(frozen=True)
class DetectionFinding:
    alert_type: str
    severity: str
    title: str
    description: str


def _already_alerted_recently(db: Session, alert_type: str, source_ip: str) -> bool:
    cutoff = datetime.now(timezone.utc) - timedelta(seconds=settings.alert_cooldown_seconds)
    stmt = (
        select(Alert.id)
        .where(
            Alert.alert_type == alert_type,
            Alert.source_ip == source_ip,
            Alert.created_at >= cutoff,
        )
        .limit(1)
    )
    return db.execute(stmt).scalar_one_or_none() is not None


def _persist_alert(db: Session, source_ip: str, finding: DetectionFinding) -> Alert | None:
    if _already_alerted_recently(db, finding.alert_type, source_ip):
        return None

    alert = Alert(
        alert_type=finding.alert_type,
        severity=finding.severity,
        source_ip=source_ip,
        title=finding.title,
        description=finding.description,
    )
    db.add(alert)
    db.flush()

    alert_logger.warning(
        "type=%s severity=%s source_ip=%s title=%r description=%r",
        finding.alert_type,
        finding.severity,
        source_ip,
        finding.title,
        finding.description,
    )
    return alert


def detect_for_attempt(db: Session, attempt: LoginAttempt) -> list[Alert]:
    now = datetime.now(timezone.utc)
    findings: list[DetectionFinding] = []

    brute_cutoff = now - timedelta(seconds=settings.brute_force_window_seconds)
    brute_count_stmt = select(func.count(LoginAttempt.id)).where(
        LoginAttempt.source_ip == attempt.source_ip,
        LoginAttempt.created_at >= brute_cutoff,
    )
    brute_count = int(db.execute(brute_count_stmt).scalar_one())
    if brute_count >= settings.brute_force_threshold:
        findings.append(
            DetectionFinding(
                alert_type="BRUTE_FORCE",
                severity="HIGH",
                title="Possible brute-force authentication attack",
                description=(
                    f"Observed {brute_count} login attempts from {attempt.source_ip} "
                    f"within {settings.brute_force_window_seconds} seconds."
                ),
            )
        )

    spray_cutoff = now - timedelta(seconds=settings.username_spray_window_seconds)
    spray_stmt = select(func.count(func.distinct(LoginAttempt.username))).where(
        LoginAttempt.source_ip == attempt.source_ip,
        LoginAttempt.created_at >= spray_cutoff,
    )
    unique_users = int(db.execute(spray_stmt).scalar_one())
    if unique_users >= settings.username_spray_threshold:
        findings.append(
            DetectionFinding(
                alert_type="USERNAME_SPRAY",
                severity="HIGH",
                title="Possible username spraying activity",
                description=(
                    f"Observed attempts against {unique_users} distinct usernames from "
                    f"{attempt.source_ip} within {settings.username_spray_window_seconds} seconds."
                ),
            )
        )

    rapid_cutoff = now - timedelta(seconds=settings.rapid_request_window_seconds)
    rapid_stmt = select(func.count(LoginAttempt.id)).where(
        LoginAttempt.source_ip == attempt.source_ip,
        LoginAttempt.created_at >= rapid_cutoff,
    )
    rapid_count = int(db.execute(rapid_stmt).scalar_one())
    if rapid_count >= settings.rapid_request_threshold:
        findings.append(
            DetectionFinding(
                alert_type="RAPID_REQUESTS",
                severity="MEDIUM",
                title="High-rate login activity detected",
                description=(
                    f"Observed {rapid_count} login attempts from {attempt.source_ip} "
                    f"within {settings.rapid_request_window_seconds} seconds."
                ),
            )
        )

    if attempt.username.strip().lower() in settings.high_value_username_set:
        findings.append(
            DetectionFinding(
                alert_type="HIGH_VALUE_ACCOUNT_ATTEMPT",
                severity="MEDIUM",
                title="High-value account name targeted",
                description=(
                    f"A login attempt from {attempt.source_ip} targeted the username "
                    f"{attempt.username!r}."
                ),
            )
        )

    alerts: list[Alert] = []
    for finding in findings:
        alert = _persist_alert(db, attempt.source_ip, finding)
        if alert is not None:
            alerts.append(alert)

    db.commit()
    return alerts
