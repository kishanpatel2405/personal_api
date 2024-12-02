from pydantic import BaseModel
from typing import List


class CleanTempResponse(BaseModel):
    cleaned_files: int
    errors: List[str]
