import uuid, enum
from sqlalchemy import String, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.db import Base

class UserRole(str, enum.Enum):
    super_admin = "super_admin"
    admin = "admin"
    restaurant_owner = "restaurant_owner"

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.restaurant_owner, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)