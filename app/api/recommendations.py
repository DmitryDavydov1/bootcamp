from fastapi import APIRouter

from app.services.recommendation_service import generate_recommendations

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.post("/generate")
def generate():
    result = generate_recommendations()
    return result