from fastapi import APIRouter

from repositories.main_db import db_manager

from models.basemodels import BaseSchema
router = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)

@router.get("/")
async def get_tickets():
    return [{"ticket_id": 1, "status": "open"}]




@router.post("/create")
async def create_ticket(data: BaseSchema.User):
    email = data.email
    try:
        users = await db_manager.get_users_by_mail(email)
        if not users:
            return {"error": "No user found with this email."}
    except Exception as e:  
        return {"error": str(e)}
    try:
        if await db_manager.create_ticket(user_name=users[0]['username']):
            return {"message": f"Ticket for user {users[0]['username']} created successfully."}
        return {"error": "Failed to create ticket."}
    except Exception as e:
        return {"error": str(e)}
    
@router.post("/posts-massage")
async def post_message():
    return {"message": "This endpoint is under construction."}

        
    
