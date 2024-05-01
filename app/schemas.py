from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    profile_image: str
    kakao_id: int

class Token(BaseModel):
    access_token: str
    token_type: str

