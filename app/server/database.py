import os
from uuid import UUID, uuid4

from bson import Binary

import motor.motor_asyncio
from bson.objectid import ObjectId

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["DB_URL"], uuidRepresentation="standard")

database = client.skill

skill_collection = database.get_collection("skill_collections")
user_collection = database.get_collection("user_collections")


def skill_helper(skill) -> dict:
    return {
        "id": str(skill["_id"]),
        "name": skill["name"],
        "year": skill["year"],

    }


def user_helper(user) -> dict:


    return {
        "UserId": user["UserId"],
        "FirstName": user["FirstName"],
        "LastName": user["LastName"],
        "Email": user["Email"],
        "Skills": [{skill["name"]: skill["year"]} for skill in user["Skills"]]
    }


async def add_skill(skill_data: dict) -> dict:
    skill = await skill_collection.insert_one(skill_data)
    new_skill = await skill_collection.find_one({"_id": skill.inserted_id})
    return skill_helper(new_skill)


async def retrieve_skills():
    skills = []
    async for skill in skill_collection.find():
        skills.append(skill_helper(skill))
    return skills


async def update_skill(id: str, data: dict):
    if len(data) < 1:
        return False
    skill = await skill_collection.find_one({"_id": ObjectId(id)})
    if skill:
        updated_skill = await skill_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_skill:
            return True
        return False


async def delete_skill(id: str):
    skill = await skill_collection.find_one({"_id": ObjectId(id)})
    if skill:
        await skill_collection.delete_one({"_id": ObjectId(id)})
        return True


async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


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
