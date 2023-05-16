from datetime import datetime

from pydantic import BaseModel


class UserCredentials(BaseModel):
    email: str
    password: str


class UserProfile(BaseModel):
    first_name: str
    last_name: str | None = None
    bio: str | None = None
    username: str | None = None


class User(BaseModel):
    id: int
    created_at: datetime
    profile: UserProfile


class UserSession(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    expires_on: datetime
