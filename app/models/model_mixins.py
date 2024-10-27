from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class UUIDMixin(SQLModel):
    uuid: UUID = Field(default_factory=uuid4, primary_key=True)
