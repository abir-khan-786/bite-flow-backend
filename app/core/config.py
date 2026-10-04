import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "RestoCore SaaS RMS"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # JWT Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY_CHANGE_IN_PRODUCTION_123456")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # ৭ দিনের জন্য ভ্যালিড থাকবে

settings = Settings()