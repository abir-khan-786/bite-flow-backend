import os
SECRET_KEY = os.getenv("SECRET_KEY", "bite-flow-super-secret-key-change-in-prod-change-it")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7