from fastapi import HTTPException
from sqlmodel import SQLModel

from app.db.db_interactions import DBInteractionsManager


async def get_object_or_404(
    model: SQLModel, relationship_names: list = [], **kwargs
) -> SQLModel:
    """
    This function attempts to fetch a record from the database based on the
    provided model and search criteria. If the record is not found,
    it raises an HTTP 404 exception.

    Args:
        model (SQLModel): The SQLModel class representing the database table\
        to query.
        relationship_names (list): A list of relationship names to be included\
        in the query.
        **kwargs: Arbitrary keyword arguments used as search criteria for the\
        database query.

    Returns:
        SQLModel: The retrieved database object if found.

    Raises:
        HTTPException: A 404 error if the object is not found in the database.
    """
    result: SQLModel | None = await DBInteractionsManager.get_record_from_db(
        kwargs, needed_model=model, relationship_names=relationship_names
    )
    if not result:
        raise HTTPException(
            status_code=404, detail=f"{model.__name__} not found."
        )
    return result
