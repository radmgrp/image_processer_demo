from api.utils import process_image_with_model
from fastapi import APIRouter, HTTPException
from starlette import status
from api.schemas import ImageSchema

router = APIRouter()


@router.post(path='/process_image/', summary='Image processing endpoint', status_code=status.HTTP_202_ACCEPTED)
async def process_image(raw_image: ImageSchema):
    """Endpoint for image processing. Accepts base64 string of an original image passed,
    after processing returns base64 string of processed image"""
    try:
        processed_image_base64_string = process_image_with_model(original_image_filename='uploaded_file',
                                                                 processed_image_filename='processed_file',
                                                                 original_image_base64=raw_image.raw_image_base64)
        return processed_image_base64_string
    except:
        raise HTTPException(status_code=400, detail="Image is invalid, please try another one")
