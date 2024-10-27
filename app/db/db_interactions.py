from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import Select
from sqlmodel import SQLModel, select

from app.db.db import async_session_decorator


class DBInteractionsManager:

    @staticmethod
    @async_session_decorator
    async def get_record_from_db(
        serializer_data: dict,
        needed_model: SQLModel,
        session: AsyncSession,
        relationship_names: list[str] = [],
    ):
        sql_query: Select = select(needed_model)
        for name in relationship_names:
            if not hasattr(needed_model, name):
                raise AttributeError(
                    (
                        f"Model {needed_model.__name__} does not have "
                        f"relationship {name}."
                    )
                )
            sql_query = sql_query.options(
                selectinload(getattr(needed_model, name))
            )
        sql_query = sql_query.filter_by(**serializer_data)

        db_result: Result = await session.execute(sql_query)
        return db_result.scalar()

    @staticmethod
    @async_session_decorator
    async def create_record_in_db(
        serializer_data: dict, needed_model: SQLModel, session: AsyncSession
    ):
        model: SQLModel = needed_model(**serializer_data)
        session.add(model)
        try:
            await session.commit()
            return "Successfully created!"
        except IntegrityError:
            return None

    @staticmethod
    @async_session_decorator
    async def update_record_in_db(
        model_object: SQLModel, fields_to_change: dict, session: AsyncSession
    ):
        for field, value in fields_to_change.items():
            if not hasattr(model_object, field):
                raise AttributeError(
                    (
                        f"Model {model_object.__name__} does not have "
                        f"attribute {field}."
                    )
                )
            setattr(model_object, field, value)
            session.add(model_object)
            await session.commit()
            await session.refresh(model_object)

    @staticmethod
    @async_session_decorator
    async def delete_record_from_db(
        model_object: SQLModel, session: AsyncSession
    ):
        await session.delete(model_object)
        await session.commit()
