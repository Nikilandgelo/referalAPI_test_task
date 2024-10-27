from uuid import UUID

from sqlmodel import Field, Relationship

from app.models.model_mixins import UUIDMixin
from app.models.user import User
from app.serializers.referral_code import ReferralCodeSerializer


class ReferralCode(UUIDMixin, ReferralCodeSerializer, table=True):
    owner_uuid: UUID = Field(foreign_key="user.uuid")
    owner: User = Relationship(
        back_populates="referral_code",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
