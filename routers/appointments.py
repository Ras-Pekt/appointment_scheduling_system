from fastapi import APIRouter

appointments_router = APIRouter(
    prefix="/appointments",
    tags=["appointments"],
)


@appointments_router.get("/")
async def get_appointments():
    return {"message": "Get all appointments"}
