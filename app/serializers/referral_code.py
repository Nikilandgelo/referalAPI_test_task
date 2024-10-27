from datetime import datetime

from sqlmodel import Field, SQLModel


class ReferralCodeSerializer(SQLModel):
    code: str = Field(max_length=255, unique=True)
    expiration_time: datetime = Field()
