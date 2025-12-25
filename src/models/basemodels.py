from pydantic import BaseModel

class BaseSchema(BaseModel):


    class User(BaseModel):
        email: str
        role: str