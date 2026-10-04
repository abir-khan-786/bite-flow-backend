from fastapi import APIRouter, HTTPException, status, Depends
from app.core.database import db
from app.core.security import hash_password, verify_password, create_access_token
from app.modules.auth.schemas import RestaurantRegisterSchema, LoginSchema, TokenResponse
from app.modules.auth.dependencies import get_current_user
from prisma.enums import UserRole
from prisma.models import User

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.post("/register-restaurant", status_code=status.HTTP_201_CREATED)
async def register_restaurant(data: RestaurantRegisterSchema):
    existing_user = await db.user.find_unique(where={"email": data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User email already exists!")

    existing_slug = await db.restaurant.find_unique(where={"slug": data.slug})
    if existing_slug:
        raise HTTPException(status_code=400, detail="Restaurant slug already taken!")

    hashed_pwd = hash_password(data.password)

    new_restaurant = await db.restaurant.create(
        data={
            "name": data.restaurant_name,
            "slug": data.slug,
            "email": data.email,
            "phone": data.phone,
            "users": {
                "create": [
                    {
                        "name": data.owner_name,
                        "email": data.email,
                        "password": hashed_pwd,
                        "role": UserRole.RESTAURANT_OWNER
                    }
                ]
            }
        },
        include={"users": True}
    )

    owner = new_restaurant.users[0]
    token = create_access_token(subject=owner.id)

    return {
        "success": True,
        "message": "Restaurant registered successfully",
        "access_token": token,
        "restaurant_id": new_restaurant.id
    }

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginSchema):
    user = await db.user.find_unique(where={"email": data.email})
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(subject=user.id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "restaurantId": user.restaurantId
        }
    }

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user