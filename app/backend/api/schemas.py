from pydantic import BaseModel


class ImageSchema(BaseModel):
    """Schema to validate the base64string"""
    raw_image_base64: str
