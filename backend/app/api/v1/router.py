from fastapi import APIRouter

from app.api.v1 import auth
from app.api.v1 import exams
from app.api.v1 import results
from app.api.v1 import progress
from app.api.v1 import history
from app.api.v1 import admin

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(exams.router)
api_router.include_router(results.router)
api_router.include_router(progress.router)
api_router.include_router(history.router)
api_router.include_router(admin.router)
