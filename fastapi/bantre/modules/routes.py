from fastapi import APIRouter

from bantre.modules.article import article_controller
from bantre.modules.auth import auth_controller


# Handles "/v1/*"
v1_router = APIRouter()
# v1_router.include_router(article_controller.article_router, prefix="/article")
v1_router.include_router(auth_controller.auth_router, prefix="/auth")
