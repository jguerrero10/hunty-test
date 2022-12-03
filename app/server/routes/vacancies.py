from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    retrieve_vacancies,
    retrieve_vacancy,
    add_vacancy,
    update_vacancy,
    delete_vacancy
)
from server.models.VacancyModel import VacancySchema
from server.response_model import response_model, error_response_model

router = APIRouter()


@router.get("/", response_description="get all vacancies")
async def get_vacancies():
    vacancies = await retrieve_vacancies()
    if vacancies:
        return response_model(vacancies, "list of all vacancies")
    return response_model(vacancies, "No vacancy")


@router.get("/{VacancyId}", response_description="get a vacancy")
async def get_vacancy_data(vacancyid):
    vacancy = await retrieve_vacancy(vacancyid)
    if vacancy:
        return response_model(vacancy, "vacancy found")
    return error_response_model("An error occurred", 404, "vacancy no found.")


@router.post("/", response_description="Datos vacancy add")
async def add_vacancy_data(vacancy: VacancySchema = Body(...)):
    vacancy = jsonable_encoder(vacancy)
    new_vacancy = await add_vacancy(vacancy)
    return response_model(new_vacancy, "added vacancy.")


@router.put("/{VacancyId}")
async def update_vacancy_data(vacancyid: str, vacancy: VacancySchema.as_optional() = Body(...)):
    vacancy = {key: value for key, value in vacancy.dict().items() if value is not None}
    updated_vacancy = await update_vacancy(vacancyid, vacancy)
    if updated_vacancy:
        return response_model(
            f"the vacancy with id {vacancyid} is updated",
            "the vacancy was updated successfully",
        )
    return error_response_model(
        "an error occurred",
        404,
        "The vacancy does not exist",
    )


@router.delete("/{VacancyId}", response_description="Vacancy data deleted from the database")
async def delete_user_data(vacancyid: str):
    deleted_vacancy = await delete_vacancy(vacancyid)
    if deleted_vacancy:
        return response_model(f'Vacancy with ID: {vacancyid} is removed', "Vacancy deleted successfully")
    return error_response_model(
        f"An error occurred", 404, f"Vacancy with id {vacancyid} doesn't exist"
    )
