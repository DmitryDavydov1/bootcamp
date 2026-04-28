from fastapi import APIRouter

from app.services.recommendation_service import generate_recommendations
from app.services.current_top_service import get_current_top, save_current_top


router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.post("/generate")
def generate():
    result = generate_recommendations()
    return result


@router.get("/current-top")
def current_top():
    return get_current_top()


@router.post("/current-top")
def save_current_top_order(data: dict):
    return save_current_top(data)