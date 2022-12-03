from fastapi import FastAPI

from server.routes.skills import router as SkillRouter
from server.routes.users import router as UserRouter

app = FastAPI()

app.include_router(SkillRouter, tags=["Skill"], prefix="/skill")
app.include_router(UserRouter, tags=["user"], prefix="/user")

@app.get("/", tags=['root'])
async def read_root():
    return {"message": "Welcome to HuntyApp"}
