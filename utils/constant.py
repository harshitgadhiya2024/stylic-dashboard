import os
from dotenv import load_dotenv
import uuid
from datetime import datetime

secreat_key = str(uuid.uuid4())
print(f"{datetime.utcnow()}: Secreat key of stylic backend: {secreat_key}")

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL") or "mongodb+srv://infostylicai:gUgH6G9oDimFRWIS@stylicai.tio3ghn.mongodb.net/"

constant_dict = {
    "mongo_url": MONGO_URL,
    "secreat_key": secreat_key,
    "openai_key": os.getenv("OPENAI_KEY"),
    "domain_url": "https://app.stylic.ai",
    "smtp_server": "smtp.hostinger.com",
    "smtp_port": 587,
    "email_address": "info@stylic.ai",
    "email_password": "Har@#0401",
    "gemini_api_key": os.getenv("GEMINI_API_KEY"),
    "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
    "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "AWS_REGION": os.getenv("AWS_REGION"),
    "S3_BUCKET_NAME": os.getenv("S3_BUCKET_NAME"),
    "S3_UPLOAD_FOLDER": os.getenv("S3_UPLOAD_FOLDER")
}