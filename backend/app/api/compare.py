from fastapi import APIRouter

router = APIRouter(
    prefix="/compare",
    tags=["comparison"]
)

@router.get("/")
async def compare_items():
    return {"message": "Comparison endpoint"}
