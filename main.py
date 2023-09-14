from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

# Instantiate the FastAPI app
app = FastAPI()


@app.get("/", description="Root Route")
async def root():
    return {"message": "Hello World"}


@app.post("/")
async def post():
    return {"message": "Hello from the post route"}


@app.get("/users")
async def list_users():
    return {"message": "List users"}


# must place specific static endpoint above the dynamic endpoints
@app.get("users/me", description="Get current user")
async def get_current_user():
    return {"message": "Current user"}


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    return {"user_id": user_id}


# examples of 'typing'
class FoodEnum(str, Enum):
    pizza = "pizza"
    pasta = "pasta"
    salad = "salad"


@app.get("/foods/{food_name}")
async def get_food_name(food_name: FoodEnum):
    if food_name == FoodEnum.pizza:
        return {"message": "Pizza is great!"}

    if food_name == FoodEnum.pasta:
        return {"message": "Pasta is great!"}

    if food_name == FoodEnum.salad:
        return {"message": "Salad is great!"}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items")
async def list_items(
    skip: int = 0, limit: int = 10
):  # setting default query param values
    return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}")
async def get_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(
    user_id: str, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# creating a Model class for Item
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/{item_id}")
async def create_item(item: Item) -> Item:  # enforcing the type
    item_dict = item.model_dump() # can call the model_dump() method on any defined models to convert to dict
    if item.tax:  # gets the attribute of the class
        item_dict.update({"price_with_tax": item.price + item.tax})
    return item_dict


@app.put("/items/{item_id}")
