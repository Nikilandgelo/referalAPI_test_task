from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship

from app.serializers.user import UserInSerializer

if TYPE_CHECKING:
    from app.models.referral_code import ReferralCode
    from app.models.user import User    # noqa: F811


class User(UserInSerializer, table=True):               # noqa: F811
    referral_code: "ReferralCode" = Relationship(
        back_populates="owner",
        cascade_delete=True,
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    # begin recursive relationship:
    referrer_uuid: UUID | None = Field(
        foreign_key="user.uuid", default=None, nullable=True
    )
    # we dont pass here cascade_delete=True because we don`t want to delete
    # referrals users when their referrer user was deleted
    referrer: "User" = Relationship(
        back_populates="referrals",
        sa_relationship_kwargs={
            "remote_side": "User.uuid",
            "lazy": "selectin",
        },
    )

    # our lookup field
    referrals: list["User"] = Relationship(
        back_populates="referrer", sa_relationship_kwargs={"lazy": "selectin"}
    )
