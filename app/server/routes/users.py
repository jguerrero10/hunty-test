from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import retrieve_users, add_user, update_user, delete_user

from server.models.UserModel import UserSchema, UserUpdateModel
from server.models.ResponseModel import response_model, error_response_model

router = APIRouter()


@router.get("/", response_description="Users retrieved")
async def get_users():
    users = await retrieve_users()
    if users:
        return response_model(users, "Se consiguieron los datos de los usuarios")
    return response_model(users, "Vacia")


@router.post("/", response_description="User data added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return response_model(new_user, "User added successfully.")


@router.put('/{UserId}')
async def update_user_data(userid: str, user: UserUpdateModel = Body(...)):
    user = {key: value for key, value in user.dict().items() if value is not None}
    updated_user = await update_user(userid, user)
    if updated_user:
        return response_model(
            f'Se actualizó el skill {userid}',
            'Skill es actualizado correctamente'
        )
    return error_response_model(
        "Error al guardar",
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
