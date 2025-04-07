from fastapi import APIRouter

doctors_router = APIRouter(
    prefix="/doctors",
    tags=["doctors"],
)


@doctors_router.get("/")
async def get_doctors():
    return {"message": "Get all doctors"}
