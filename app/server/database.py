import os
from uuid import UUID, uuid4

from urllib.parse import quote_plus
import motor.motor_asyncio
from server.helpers import user_helper, vacancy_helper

username = quote_plus(os.environ["DB_USER"])
password = quote_plus(os.environ["DB_PASS"])

client = motor.motor_asyncio.AsyncIOMotorClient(f'mongodb+srv://{username}:{password}@cluster0.htzlfvi.mongodb.net/?retryWrites=true&w=majority', uuidRepresentation="standard")

database = client.skill

user_collection = database.get_collection("user_collections")
vacancy_collection = database.get_collection("vacancy_collections")


def comparison(dict1: dict, dict2: dict) -> bool:
    amount = 0
    for i in dict1:
        for j in dict2:
            if i['name'] in j.values():
                if i['year'] >= j['year']:
                    amount += 1
    if amount * 100 / len(dict2) >= 50:
        return True
    return False


async def match_vacancies(userid: UUID):
    match = []
    user_data = await user_collection.find_one({"UserId": userid})
    s = [i['name'] for i in user_data["Skills"]]
    if user_data:
        async for vacancy in vacancy_collection.find(
                {"RequiredSkills.name": {'$in': s}}).collation({'locale': 'en', 'strength': 2}):
            if comparison(user_data["Skills"], vacancy["RequiredSkills"]):
                match.append(vacancy_helper(vacancy))
            pass
    return match


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
