from fastapi import FastAPI

from server.routes.users import router as UserRouter
from server.routes.vacancies import router as VacancyRouter

app = FastAPI()

app.include_router(UserRouter, tags=["user"], prefix="/user")
app.include_router(VacancyRouter, tags=["vancancy"], prefix='/vacancy')


@app.get("/", tags=['root'])
async def read_root():
    return {"message": "Welcome to HuntyApp"}
