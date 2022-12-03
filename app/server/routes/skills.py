from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import add_skill, retrieve_skills, update_skill, delete_skill
from server.models.SkillModel import SkillSchema, UpdateSkill
from server.models.ResponseModel import response_model, error_response_model

router = APIRouter()


@router.post("/", response_description="Datos de skill agregados a la base de datos")
async def add_skill_data(skill: SkillSchema = Body(...)):
    skill = jsonable_encoder(skill)
    new_skill = await add_skill(skill)
    return response_model(new_skill, "Skill agregado.")


@router.get("/", response_description="Skill retrieved")
async def get_skills():
    skills = await retrieve_skills()
    if skills:
        return response_model(skills, "Se muestran todos los skills")
    return response_model(skills, "ista vacía")


@router.put('/{id}')
async def update_skill_data(id: str, skill: UpdateSkill = Body(...)):
    skill = {key: value for key, value in skill.dict().items() if value is not None}
    updated_skill = await update_skill(id, skill)
    if updated_skill:
        return response_model(
            f'Se actualizó el skill {id}',
            'Skill es actualizado correctamente'
        )
    return error_response_model(
        "Error al guardar",
        404,
        "Error"
    )


@router.delete("/{id}", response_description="skill data deleted from the database")
async def delete_skill_data(id: str):
    deleted_socie = await delete_skill(id)
    if deleted_socie:
        return response_model(
            f"Skill con ID: {id} es borrado", "Skill Borrado exitosamente"
        )
    return error_response_model(
        f"Hubo un error", 404, f"Skill con id {id} no existe."
    )
