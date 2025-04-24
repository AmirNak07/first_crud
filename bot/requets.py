import jwt
import time

SECRET_KEY = "supersecret"


def generate_jwt():
    payload = {
        "bot_id": "telegram-bot",
        "exp": time.time() + 60 * 60,  # Expires in an hour
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


print(generate_jwt())
