from nosql_example.database import user_collection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional


app = FastAPI()

class User(BaseModel):
    name: str
    email: EmailStr

class UserResponse(User):
    id: str

@app.get("/users")
def read_users() ->list[UserResponse]:
    users = []
    for user in user_collection.find():
        users.append(UserResponse(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"]
))
    return users


@app.post("/user")
def create_user(
    user: User
):
    result = user_collection.insert_one(
        user.model_dump(exclude_none=True)
    )

    user_response = UserResponse(
        id = str(result.inserted_id),
        **user.model_dump()
    )
    return user_response

from bson import ObjectId

@app.get("/user")
def get_user(user_id: str):
    db_user = user_collection.find_one(
        {
            "_id":ObjectId(user_id)
            if ObjectId.is_valid(user_id)
            else None
        }
    )

    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    #user_response = UserResponse(
     #   id=str(db_user["_id"]),
    #    **db_user
    db_user["id"] = str(db_user["_id"])
    del db_user["_id"]
    return db_user
