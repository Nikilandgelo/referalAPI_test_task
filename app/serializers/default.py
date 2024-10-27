from pydantic import BaseModel


class DefaultMessageSerializer(BaseModel):
    message: str
