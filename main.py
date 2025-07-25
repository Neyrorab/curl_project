from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Модели
class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    age: Optional[int] = None

class UserInDB(User):
    id: int

# Хранилище
users_db = []
current_id = 1

# Корень
@app.get("/")
def root():
    return {"message": "Welcome to the User Directory!"}

# CREATE
@app.post("/users/", response_model=UserInDB)
def create_user(user: User):
    global current_id
    user_in_db = UserInDB(id=current_id, **user.dict())
    users_db.append(user_in_db)
    current_id += 1
    return user_in_db

# READ все
@app.get("/users1/", response_model=List[UserInDB])
def get_users():
    return users_db

# READ по ID
@app.get("/users/{user_id}", response_model=UserInDB)
def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# UPDATE
@app.put("/users/{user_id}", response_model=UserInDB)
def update_user(user_id: int, updated_user: User):
    for user in users_db:
        if user.id == user_id:
            user.first_name = updated_user.first_name
            user.last_name = updated_user.last_name
            user.email = updated_user.email
            user.age = updated_user.age
            return user
    raise HTTPException(status_code=404, detail="User not found")

# DELETE
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for idx, user in enumerate(users_db):
        if user.id == user_id:
            users_db.pop(idx)
            return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")
