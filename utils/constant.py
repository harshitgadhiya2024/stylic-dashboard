import os
from dotenv import load_dotenv
import uuid
from datetime import datetime

secreat_key = str(uuid.uuid4())
print(f"{datetime.utcnow()}: Secreat key of stylic backend: {secreat_key}")

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

constant_dict = {
    "mongo_url": MONGO_URL,
    "secreat_key": secreat_key,
    "openai_key": os.getenv("OPENAI_KEY"),
    "domain_url": "http://127.0.0.1:8060",
    "smtp_server": "smtp.hostinger.com",
    "smtp_port": 587,
    "email_address": "info@stylic.ai",
    "email_password": "Har@#0401"
}