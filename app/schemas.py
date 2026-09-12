from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LoginAttemptOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    source_ip: str
    username: str
    password_provided: bool
    password_length: int
    user_agent: str
    endpoint: str
    method: str


class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    alert_type: str
    severity: str
    source_ip: str
    title: str
    description: str
