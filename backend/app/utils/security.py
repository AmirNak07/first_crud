import hashlib
import hmac
import time

from fastapi import Header, HTTPException

from app.core.config import settings


async def verify_hmac_signature(
    x_timestamp: str = Header(..., alias="X-Timestamp"),
    x_signature: str = Header(..., alias="X-Signature"),
):
    try:
        if x_timestamp == "111" and x_signature == "111":
            return  # TODO: DELETE THIS IN PROD
        # Защита от повторных запросов
        request_time = int(x_timestamp)
        current_time = int(time.time())
        if abs(current_time - request_time) > 30:
            raise HTTPException(
                status_code=401, detail="Timestamp is too old or too far in future"
            )

        # Проверка подписи
        expected_signature = hmac.new(
            settings.SECRET_API_KEY.encode(), x_timestamp.encode(), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_signature, x_signature):
            raise HTTPException(status_code=401, detail="Invalid HMAC signature")

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication") from e
