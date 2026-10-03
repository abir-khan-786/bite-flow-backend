from fastapi import Depends, Header, HTTPException
from jose import jwt
from app.core.security import SECRET_KEY, ALGORITHM
from app.db import CentralSessionLocal, get_tenant_engine
from sqlalchemy import text
from typing import Annotated

# 1. এটা ঠিক করলাম - alias দিয়ে
async def get_current_restaurant(
    x_restaurant_slug: Annotated[str, Header(alias="x-restaurant-slug")]
):
    async with CentralSessionLocal() as session:
        result = await session.execute(
            text("SELECT db_url_encrypted FROM restaurants WHERE slug=:slug"),
            {"slug": x_restaurant_slug}
        )
        row = result.first()
        if not row:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        decrypted_url = row[0] # পরে এখানে decrypt() বসাবি

        if not decrypted_url:
            raise HTTPException(status_code=500, detail="DB URL is empty")

        tenant_engine = get_tenant_engine(decrypted_url)
        return tenant_engine

# 2. এটাও ঠিক করলাম - Bearer token handle
async def get_current_user(
    authorization: Annotated[str, Header(alias="Authorization")]
):
    try:
        # "Bearer <token>" থেকে token আলাদা করা
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid auth format")

        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")