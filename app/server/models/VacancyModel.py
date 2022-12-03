from typing import List, Optional

from pydantic import BaseModel, Field, create_model
import uuid as uuid_pkg

from pydantic.networks import HttpUrl

from server.models.CompanyModel import CompanySchema
from server.models.SkillModel import SkillSchema


class VacancySchema(BaseModel):
    VacancyId: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True
    )
    CompanyName: CompanySchema = Field(...)
    PositionName: str = Field(...)
    Salary: float = Field(..., gt=0)
    Currency: str = Field(..., max_length=5, min_length=1)
    VacancyLink: HttpUrl = Field(...)
    RequiredSkills: List[SkillSchema]

    class Config:
        schema_extra = {
            "example": {
                "VacancyId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "CompanyName": {
                    "CompanyId": "b3c2c8bd-19ge-48bc-b18f-e1cf491c7718",
                    "CompanyName": "Company example",
                    "description": ""
                },
                "PositionName": "string",
                "Salary": 1,
                "Currency": "COP",
                "VacancyLink": "https://www.test.com",
                "RequiredSkills": [
                    {
                        "name": "python",
                        "year": 2
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

