from fastapi import APIRouter

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)

@router.get("/")
async def get_tickets():
    return [{"ticket_id": 1, "status": "open"}]
