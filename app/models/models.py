from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
import uuid, datetime

Base = declarative_base()

class Restaurant(Base): # central registry
    __tablename__ = "restaurants"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    slug = Column(String, unique=True, index=True)
    db_url_encrypted = Column(String) # তোর cipher.ts দিয়ে encrypt করা url
    owner_email = Column(String, unique=True)
    is_active = Column(Boolean, default=True)