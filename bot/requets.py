import hashlib
import hmac
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_API_KEY")


def generate_hmac_signature(secret: str, timestamp: str):
    msg = timestamp.encode()
    return hmac.new(secret.encode(), msg, hashlib.sha256).hexdigest()


def send_request():
    timestamp = str(int(time.time()))
    signature = generate_hmac_signature(SECRET_KEY, timestamp)

    headers = {"X-Timestamp": timestamp, "X-Signature": signature}

    response = requests.get("http://localhost:8000/users", headers=headers)
    print(response.status_code, response.json())


send_request()
