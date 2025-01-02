from typing import List

from pydantic import BaseModel


class CleanTempResponse(BaseModel):
    cleaned_files: int
    errors: List[str]
