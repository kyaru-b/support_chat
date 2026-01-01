from fastapi import APIRouter , Body

from repositories.main_db import db_manager

from models.basemodels import BaseSchema

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)
"""get"""
@router.get("/")
async def get_tickets():
    return [{"ticket_id": 1, "status": "open"}]

@router.get("/{ticket_id}/messages")
async def get_ticket_messages(ticket_id: int):
    try:
        messages = await db_manager.get_messages_by_ticket(ticket_id)
        return {"ticket_id": ticket_id, "messages": messages}
    except Exception as e:
        return {"error": str(e)}





"""post"""
@router.post("/create")
async def create_ticket(data: BaseSchema.User):
    email = data.email
    try:
        users = await db_manager.get_users_by_mail(email)
        if not users:
            return {"error": "No user found with this email."}
        
        user = users[0]
        # Check for existing open ticket
        existing_ticket = await db_manager.get_open_ticket(user['id'])
        if existing_ticket:
            return {
                "message": "Active ticket found.", 
                "ticket_id": existing_ticket['id'], 
                "user_id": user['id']
            }

    except Exception as e:  
        return {"error": str(e)}
    try:
        ticket_id = await db_manager.create_ticket(user_name=users[0]['username'])
        if isinstance(ticket_id, Exception):
            return {"error": str(ticket_id)}
        if ticket_id is not None:
            return {"message": f"Ticket for user {users[0]['username']} created successfully.", "ticket_id": ticket_id, "user_id": users[0]['id']}
        return {"error": "Failed to create ticket."}
    except Exception as e:
        return {"error": str(e)}


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
    
@router.post("/close/")
async def close_ticket(data: BaseSchema.CloseTicket):
    try:
        result = await db_manager.close_ticket(ticket_id=data.ticket_id)
        if result is None:
            return {"message": f"Ticket {data.ticket_id} closed successfully."}
        return {"error": f"{result}"}
    except Exception as e:
        return {"error": str(e)}
