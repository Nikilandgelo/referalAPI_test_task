from typing import Annotated
from uuid import UUID

from fastapi import BackgroundTasks, Depends, HTTPException

from app.core.objects_getter import get_user_from_jwt
from app.core.referral_codes import generate_new_referral_code
from app.core.security import verify_ownership
from app.db.db_interactions import DBInteractionsManager
from app.db.db_shortcuts import get_object_or_404
from app.models.referral_code import ReferralCode
from app.models.user import User
from app.routes import referral_code_router
from app.serializers.default import DefaultMessageSerializer
from app.serializers.referral_code import ReferralCodeSerializer
from app.serializers.user import ReferralsSerializer


@referral_code_router.post(
    "/",
    response_model=DefaultMessageSerializer,
    responses={
        404: {"description": "User not found."},
        401: {"description": "Invalid token."},
    },
    summary="Create Referral Code",
    description="Generate a new referral code for the given user.",
)
async def create_referral_code(
    user: Annotated[User, Depends(get_user_from_jwt)],
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(generate_new_referral_code, user)
    return DefaultMessageSerializer(
        message="Referral code created successfully."
    )


@referral_code_router.get(
    "/",
    response_model=ReferralCodeSerializer,
    summary="Get Referral Code by Email",
    description="Get the referral code associated with the given user's email."
)
async def get_referral_code_by_email(email: str):
    user: User = await get_object_or_404(User, email=email)
    referral_code: ReferralCode = await get_object_or_404(
        ReferralCode, owner_uuid=user.uuid
    )
    return referral_code


@referral_code_router.delete(
    "/{referral_code}",
    response_model=DefaultMessageSerializer,
    responses={
        401: {"description": "Invalid token."},
        403: {"description": "You are not the owner of this referral code."},
        404: {"description": "User or Referral code not found."},
    },
    summary="Delete Referral Code",
    description=(
        "Delete the referral code associated with the given " "referral code."
    ),
)
async def delete_referral_code(
    referral_code: str,
    user: Annotated[User, Depends(get_user_from_jwt)],
    background_tasks: BackgroundTasks,
):
    referral_code: ReferralCode = await get_object_or_404(
        ReferralCode, code=referral_code
    )
    verify_ownership(referral_code, "owner_uuid", user.uuid)
    background_tasks.add_task(
        DBInteractionsManager.delete_record_from_db, referral_code
    )
    return DefaultMessageSerializer(
        message="Referral code deleted successfully."
    )


@referral_code_router.post(
    "/become_referral",
    response_model=DefaultMessageSerializer,
    responses={
        400: {"description": "You can not become a referral of your own."},
        401: {"description": "Invalid token."},
        404: {"description": "User or Referral code not found."},
    },
    summary="Become Referral",
    description="Make the given user a referral of the user from ref code.",
)
async def become_referral(
    ref_code: str,
    user: Annotated[User, Depends(get_user_from_jwt)],
    background_tasks: BackgroundTasks,
):
    referral_code: ReferralCode = await get_object_or_404(
        ReferralCode, code=ref_code
    )
    if referral_code.owner_uuid == user.uuid:
        raise HTTPException(
            status_code=400, detail="You cannot become a referral of your own."
        )
    background_tasks.add_task(
        DBInteractionsManager.update_record_in_db,
        user,
        {"referrer_uuid": referral_code.owner_uuid},
    )
    return DefaultMessageSerializer(message="You became a referral.")


@referral_code_router.get(
    "/all_referrals/{uuid_referrer}",
    response_model=ReferralsSerializer,
    responses={404: {"description": "User not found."}},
    summary="Get All Referrals",
    description="Get all users who referred the user with the given UUID.",
)
async def get_all_referrals(uuid_referrer: UUID):
    user: User = await get_object_or_404(
        User, relationship_names=["referrals"], uuid=uuid_referrer
    )
    return ReferralsSerializer(referrals=user.referrals)
