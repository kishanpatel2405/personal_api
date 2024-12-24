import os
import shutil

from fastapi import APIRouter, HTTPException

from schemas.v1.clean_temp import CleanTempResponse

router = APIRouter()


@router.post("", response_model=CleanTempResponse, name="clean_temp", status_code=200)
async def clean_temp_files():
    temp_directories = [
        "C:/Windows/Temp",
        "/tmp",
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
                            os.remove(file_path)
                            cleaned_files_count += 1
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

    if cleaned_files_count == 0 and errors:
        raise HTTPException(status_code=500, detail="Failed to clean temporary files.")

    return CleanTempResponse(
        cleaned_files=cleaned_files_count,
        errors=errors,
    )
