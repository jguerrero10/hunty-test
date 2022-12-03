from typing import Optional

from pydantic import BaseModel, Field


class SkillSchema(BaseModel):
    name: str = Field(...)
    year: int = Field(..., gt=0)

    class Config:
        schema_extra = {
            "example": {
                "name": "python",
                "year": 2
            }
        }


class UpdateSkill(BaseModel):
    name: Optional[str]
    year: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "name": "python",
                "year": 2
            }
        }

