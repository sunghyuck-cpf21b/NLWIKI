from pydantic import BaseModel, field_validator


class ImageB64(BaseModel):
    data: str