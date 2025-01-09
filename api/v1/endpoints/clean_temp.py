import os
import shutil

from fastapi import APIRouter, HTTPException

from schemas.v1.clean_temp import CleanTempResponse
from services.clean_temp import attempt_delete

router = APIRouter()


@router.post("", response_model=CleanTempResponse, name="clean_temp", status_code=200)
async def clean_temp_files():
    temp_directories = [
        r"C:\Users\kisha\AppData\Local\Temp"
    ]

    cleaned_files_count = 0
    errors = []

    for temp_dir in temp_directories:
        if os.path.exists(temp_dir):
            try:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            if attempt_delete(file_path):
                                cleaned_files_count += 1
                            else:
                                errors.append(f"Error deleting {file_path}: File is in use or permission denied.")
                        except Exception as e:
                            errors.append(f"Error deleting {file_path}: {str(e)}")

                    for dir in dirs:
                        try:
                            dir_path = os.path.join(root, dir)
                            shutil.rmtree(dir_path)
                        except Exception as e:
                            errors.append(f"Error deleting {dir_path}: {str(e)}")
            except Exception as e:
                errors.append(f"Error accessing {temp_dir}: {str(e)}")
        else:
            errors.append(f"Temp directory {temp_dir} not found or inaccessible.")

    if errors:
        return CleanTempResponse(
            cleaned_files=cleaned_files_count,
            errors=errors,
        )

    if cleaned_files_count == 0:
        return CleanTempResponse(
            cleaned_files=cleaned_files_count,
            errors=errors,
        )

    return CleanTempResponse(
        cleaned_files=cleaned_files_count,
        errors=errors,
    )
