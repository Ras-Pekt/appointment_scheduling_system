from fastapi import APIRouter

patients_router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)


@patients_router.get("/")
async def get_patients():
    print("Get all patients")
    return {"message": "Get all patients"}
