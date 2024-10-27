from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel

from app.models.model_mixins import UUIDMixin


class UserSerializer(UUIDMixin, SQLModel):
    email: EmailStr = Field(max_length=255, unique=True)


class UserInSerializer(UserSerializer):
    password: str = Field(min_length=8, max_length=255)


class UserOutSerializerWithToken(SQLModel):
    user: UserSerializer
    access_token: str = Field()


class ReferralsSerializer(BaseModel):
    referrals: list[UserSerializer]
