from database import user_collection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    email: str


@app.get("/users")
def read_users() ->list[User]:
    return [user for user in user_collection.find()]


@app.post("/user")
def create_user(
    user: User
):
    result = user_collection.insert_one(
        user.model_dump(exclude_none=True)
    )