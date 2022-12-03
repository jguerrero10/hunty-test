from typing import Optional

from pydantic import BaseModel, Field
import uuid as uuid_pkg


class CompanySchema(BaseModel):
    CompanyId: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True
    )
    CompanyName: str = Field(...)
    description: Optional[str] = ''

    class Config:
        schema_extra = {
            "example": {
                "CompanyId": "b3c2c8bd-19ge-48bc-b18f-e1cf491c7718",
                "CompanyName": "Company example",
                "description": ""
            }
        }
