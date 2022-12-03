from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr
import uuid as uuid_pkg

from server.models.SkillModel import SkillSchema


class UserSchema(BaseModel):
    UserId: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        alias='UserId'
    )
    FirstName: str = Field(...)
    LastName: str = Field(...)
    Email: EmailStr = Field(...)
    YearsPreviousExperience: int = Field(..., ge=0)
    Skills: List[SkillSchema]

    class Config:
        schema_extra = {
            "example": {
                "UserId": "5a4ef1e0-5a93-4b30-86b0-897062e83a52",
                "FirstName": "Test Name",
                "LastName": "Test Last Name",
                "Email": "un.test.no.hace.mal@gmail.com",
                "YearsPreviousExperience": 5,
                "Skills": [
                    {
                        "name": "python",
                        "year": 2
                    },
                    {
                        "name": "Java",
                        "year": 4
                    }
                ]
            }
        }


class UserUpdateModel(BaseModel):
    UserId: Optional[uuid_pkg.UUID] = uuid_pkg.uuid4()
    FirstName: Optional[str]
    LastName: Optional[str]
    Email: Optional[EmailStr]
    YearsPreviousExperience: Optional[int]
    Skills: Optional[List]

    class Config:
        schema_extra = {
            "example": {
                "UserId": "5a4ef1e0-5a93-4b30-86b0-897062e83a52",
                "FirstName": "Test Name",
                "LastName": "Test Last Name",
                "Email": "un.test.no.hace.mal@gmail.com",
                "YearsPreviousExperience": 5,
                "Skills": [
                    {
                        "name": "python",
                        "year": 2
                    },
                    {
                        "name": "Java",
                        "year": 4
                    }
                ]
            }
        }

