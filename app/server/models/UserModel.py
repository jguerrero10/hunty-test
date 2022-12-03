from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr, create_model
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

    @classmethod
    def as_optional(cls):
        annonations = cls.__fields__
        fields = {
            attribute: (Optional[data_type.type_], None)
            for attribute, data_type in annonations.items()
        }
        optional_model = create_model(f"Optional{cls.__name__}", **fields)
        return optional_model
