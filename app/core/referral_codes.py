from datetime import datetime, timedelta, timezone
from secrets import token_hex

from app.config.settings import Settings, get_settings
from app.db.db_interactions import DBInteractionsManager
from app.models.referral_code import ReferralCode
from app.models.user import User

settings: Settings = get_settings()


async def generate_new_referral_code(user: User) -> None:
    current_active_code: ReferralCode | None = (
        await DBInteractionsManager.get_record_from_db(
            {"owner_uuid": user.uuid}, ReferralCode
        )
    )
    if current_active_code:
        await DBInteractionsManager.delete_record_from_db(current_active_code)

    while True:
        status: str | None = await DBInteractionsManager.create_record_in_db(
            {
                "code": token_hex(16),
                "expiration_time": (
                    datetime.now(timezone.utc)
                    + timedelta(days=settings.REFERRAL_CODE_DAYS)
                ).replace(tzinfo=None),
                "owner_uuid": user.uuid,
            },
            ReferralCode,
        )
        if status:
            break
