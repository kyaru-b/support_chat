from pydantic import BaseModel

class BaseSchema(BaseModel):


    class User(BaseModel):
        email: str
        role: str

    class Ticket(BaseModel):
        user_name: str

    class Message(BaseModel):
        ticket_id: int
        email: str
        content: str
    
    class CloseTicket(BaseModel):
        ticket_id: int