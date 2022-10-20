import base64
import os
from pathlib import Path
from api.ml_model import predictor
from datetime import datetime


def get_original_image_filepath(original_image_filename: str) -> Path:
    """Util function to create filepath for saving original image file"""
    dir_path = Path(__file__).parent.parent.resolve()
    images_dirname = 'image_repo/original/'
    path_to_repo = Path(dir_path, images_dirname)
    try:
        os.makedirs(path_to_repo)
        original_image_filename = f'{original_image_filename}{datetime.now()}.jpg'
        original_image_filepath = Path(dir_path, images_dirname, original_image_filename)
        return original_image_filepath
    except:
        original_image_filename = f'{original_image_filename}{datetime.now()}.jpg'
        original_image_filepath = Path(dir_path, images_dirname, original_image_filename)
        return original_image_filepath


def get_processed_image_savepath(processed_image_filename: str) -> Path:
    """Util function to create filepath for saving processed image file"""
    dir_path = Path(__file__).parent.parent.resolve()
    processed_images_dirname = 'image_repo/processed/'
    path_to_repo = Path(dir_path, processed_images_dirname)
    try:
        os.makedirs(path_to_repo)
        processed_image_filename = f'{processed_image_filename}{datetime.now()}.jpg'
        save_path = Path(dir_path, processed_images_dirname, processed_image_filename)
        return save_path
    except:
        processed_image_filename = f'{processed_image_filename}{datetime.now()}.jpg'
        save_path = Path(dir_path, processed_images_dirname, processed_image_filename)
        return save_path


def save_original_image_as_file(original_image_base64: str, original_image_filepath: Path) -> None:
    """Util function to save original image file"""
    image_as_bytes = str.encode(original_image_base64)  # convert string to bytes
    image_recovered = base64.b64decode(image_as_bytes)  # decode base64string
    with open(original_image_filepath, "wb") as file:
        file.write(image_recovered)
    return None


def get_processed_image_base64(processed_image_filepath: Path) -> str:
    """Util function to processed image file as base64 string"""
    with open(processed_image_filepath, "rb") as file:
        processed_image_file_object = file.read()
        processed_image_base64 = base64.b64encode(processed_image_file_object)
        processed_image_base64_string = processed_image_base64.decode('ascii')
    return processed_image_base64_string


def process_image_with_model(original_image_filename: str, processed_image_filename: str,
                             original_image_base64: str) -> str:
    """Util function to go through all the steps of processing original image to processed image base64 string"""
    original_image_filepath = get_original_image_filepath(original_image_filename=original_image_filename)
    processed_image_filepath = get_processed_image_savepath(processed_image_filename=processed_image_filename)
    save_original_image_as_file(original_image_base64, original_image_filepath)
    predictor.get_prediction(img_path=original_image_filepath, save_path=processed_image_filepath)
    processed_image_base64_string = get_processed_image_base64(processed_image_filepath)
    return processed_image_base64_string
