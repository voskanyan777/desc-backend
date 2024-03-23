from pydantic import BaseModel, EmailStr, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    login: str
    password: bytes
    email: EmailStr
    active: bool = True
