from fastapi import APIRouter

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

referral_code_router = APIRouter(
    prefix="/referral_codes",
    tags=["Referral_codes"],
)

ALL_ROUTERS: list[APIRouter] = [
    value for _, value in locals().items() if isinstance(value, APIRouter)
]
