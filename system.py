from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# Example data models
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

# In-memory database
items = []
users_db = [{"username": "user1", "password": "password1", "hashed_password": "hashed_password1"}]

# Function to authenticate user
def authenticate_user(username: str, password: str):
    user = next((user for user in users_db if user["username"] == username), None)
    if not user or user["password"] != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    return user

# Dependency to get the current user
def get_current_user(username: str = Depends(authenticate_user)):
    return username

@app.post("/login/")
def login(user: User):
    # This function will only be called if the user is successfully authenticated
    return {"message": "Login successful"}

@app.post("/items/", response_model=Item)
def create_item(item: Item, current_user: UserInDB = Depends(get_current_user)):
    # Simulate database insert
    items.append(item)
    return item

@app.get("/items/", response_model=List[Item])
def read_items():
    return items

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return items[item_id]
