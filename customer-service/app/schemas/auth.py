from typing import Optional
from pydantic import BaseModel

class ResetPasswordForm(BaseModel):
    username: str
    password: str
    confirm_password: str

class ChangePasswordForm(BaseModel):
    old_password: str
    password: str
    confirm_password: str

class VerifyForm(BaseModel):
    username: str

class OtpForm(BaseModel):
    username: Optional[str] = None
    otp_code: str

class LoginForm(BaseModel):
    username: str
    password: str
    
class AuthToken(BaseModel):
    id: int

class TokenRead(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
    expire: str

class Auth(BaseModel):
    id: int
    type: str
    expire: str