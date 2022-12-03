from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import retrieve_users, retrieve_user, add_user, update_user, delete_user

from server.models.UserModel import UserSchema
from server.response_model import response_model, error_response_model

router = APIRouter()


@router.get("/", response_description="get all users")
async def get_users():
    users = await retrieve_users()
    if users:
        return response_model(users, "User data was obtained")
    return response_model(users, "There is no data")


@router.post("/", response_description="User data added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return response_model(new_user, "User added successfully.")


@router.put('/{UserId}', response_description="user data is updated from the database")
async def update_user_data(userid: str, user: UserSchema.as_optional() = Body(...)):
    user = {key: value for key, value in user.dict().items() if value is not None}
    updated_user = await update_user(userid, user)
    if updated_user:
        return response_model(
            f'Updated user {userid}',
            'User is updated successfully'
        )
    return error_response_model(
        f"Failed to save user {userid}",
        404,
        "Error"
    )


@router.delete("/{UserId}", response_description="User data deleted from the database")
async def delete_user_data(userid: str):
    deleted_user = await delete_user(userid)
    if deleted_user:
        return response_model(f'User with ID: {userid} is removed', "User deleted successfully")
    return error_response_model(
        f"An error occurred", 404, f"User with id {userid} doesn't exist"
    )
