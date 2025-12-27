from fastapi import APIRouter

from repositories.main_db import db_manager

from Utility.utils import Utils

from models.basemodels import BaseSchema

utils = Utils()
        
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/")
async def get_users():
    return [{"username": "test_user"}]


@router.post("/create")
async def create_user(user: BaseSchema.User):
    email = user.email
    role = user.role.lower()
    try:
        existing_users = await db_manager.get_users_by_mail(email)
        if existing_users: 
            return {"error": "User with this email already exists."}   
    except Exception as e:
        return []
    else:
        username = await utils.generate_username()
        try:
            if await db_manager.create_user(username, email, role)  is None:
                return {"message": f"User {username} created successfully."}
        except Exception as e:
            return {"error": str(e)}
        return {"error": "Failed to create user."}
    







