from fastapi import Request

from app.config import get_settings


settings = get_settings()


def get_client_ip(request: Request) -> str:
    if settings.trust_proxy_headers:
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip.strip()

    if request.client:
        return request.client.host

    return "unknown"
