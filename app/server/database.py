import os
from uuid import UUID, uuid4

import motor.motor_asyncio
from server.helpers import user_helper, vacancy_helper

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["DB_URL"], uuidRepresentation="standard")

database = client.skill

user_collection = database.get_collection("user_collections")
vacancy_collection = database.get_collection("vacancy_collections")


async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


async def retrieve_user(userid: UUID) -> dict:
    user = await user_collection.find_one({"UserId": userid})
    if user:
        return user_helper(user)


async def add_user(user_data: dict) -> dict:
    if 'UserId' not in user_data:
        user_data['UserId'] = uuid4()
    await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"UserId": user_data['UserId']})
    return user_helper(new_user)


async def update_user(userid: UUID, data: dict):
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"UserId": userid})
    if user:
        updated_user = await user_collection.update_one(
            {"UserId": userid}, {"$set": data}
        )
        if updated_user:
            return True
        return False


async def delete_user(userid: UUID):
    user = await user_collection.find_one({"UserId": userid})
    if user:
        await user_collection.delete_one({"UserId": userid})
        return True


async def retrieve_vacancies():
    vacancies = []
    async for vacancy in vacancy_collection.find():
        vacancies.append(vacancy_helper(vacancy))
    return vacancies


async def retrieve_vacancy(vacancyid: UUID) -> dict:
    vacancy = await vacancy_collection.find_one({"VacancyId": vacancyid})
    if vacancy:
        return vacancy_helper(vacancy)


async def add_vacancy(vacancy_data: dict) -> dict:
    if 'VacancyId' not in vacancy_data:
        vacancy_data['VacancyId'] = uuid4()
    await vacancy_collection.insert_one(vacancy_data)
    new_vacancy = await vacancy_collection.find_one({"VacancyId": vacancy_data['VacancyId']})
    return vacancy_helper(new_vacancy)


async def update_vacancy(vacancyid: UUID, data: dict):
    if len(data) < 1:
        return False
    vacancy = await vacancy_collection.find_one({"VacancyId": vacancyid})
    if vacancy:
        updated_vacancy = await vacancy_collection.update_one(
            {"VacancyId": vacancyid}, {"$set": data}
        )
        if updated_vacancy:
            return True
        return False


async def delete_vacancy(vacancyid: UUID):
    vacancy = await vacancy_collection.find_one({"VacancyId": vacancyid})
    if vacancy:
        await vacancy_collection.delete_one({"VacancyId": vacancyid})
        return True
