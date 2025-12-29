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
        result = await db_manager.create_ticket(user_name=users[0]['username'])
        if result is None:
            return {"message": f"Ticket for user {users[0]['username']} created successfully."}
        return {"error": f"{result}"}
    except Exception as e:
        return {"error": str(e)}
    
from fastapi import Body

@router.post("/post-message")
async def post_message(data: BaseSchema.Message = Body(...)):
    # Получаем id отправителя по username
    sender_user = await db_manager.get_users_by_mail(data.email)
    print(sender_user)
    if not sender_user:
        return {"error": f"User {data.email} not found"}
    sender_id = sender_user[0]["id"]
    result = await db_manager.create_message(
        ticket_id=data.ticket_id,
        sender_id=sender_id,
        text=data.content
    )
    if result is None:
        return {"message": "Message sent successfully"}
    return {"error": str(result)}
    


