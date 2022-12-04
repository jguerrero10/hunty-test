from fastapi import APIRouter

from server.database import match_vacancies
from server.response_model import response_model, error_response_model

router = APIRouter()


@router.get("/", response_description="math a vacancy")
async def match_vacancies_user(userid):
    vacancies = await match_vacancies(userid)
    if vacancies:
        return response_model(vacancies, "vacancy found")
    return error_response_model("An error occurred", 200, "vacancy no found.")
