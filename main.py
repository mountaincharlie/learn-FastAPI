from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID
from datetime import datetime, time, timedelta

# Instantiate the FastAPI app
app = FastAPI()


# @app.get("/", description="Root Route")
# async def root():
#     return {"message": "Hello World"}


# @app.post("/")
# async def post():
#     return {"message": "Hello from the post route"}


# @app.get("/users")
# async def list_users():
#     return {"message": "List users"}


# # must place specific static endpoint above the dynamic endpoints
# @app.get("users/me", description="Get current user")
# async def get_current_user():
#     return {"message": "Current user"}


# @app.get("/users/{user_id}")
# async def get_user(user_id: str):
#     return {"user_id": user_id}


# # examples of 'typing'
# class FoodEnum(str, Enum):
#     pizza = "pizza"
#     pasta = "pasta"
#     salad = "salad"


# @app.get("/foods/{food_name}")
# async def get_food_name(food_name: FoodEnum):
#     if food_name == FoodEnum.pizza:
#         return {"message": "Pizza is great!"}

#     if food_name == FoodEnum.pasta:
#         return {"message": "Pasta is great!"}

#     if food_name == FoodEnum.salad:
#         return {"message": "Salad is great!"}


# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# @app.get("/items")
# async def list_items(
#     skip: int = 0, limit: int = 10
# ):  # setting default query param values
#     return fake_items_db[skip : skip + limit]


# @app.get("/items/{item_id}")
# async def get_item(item_id: str, q: str | None = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item


# @app.get("/users/{user_id}/items/{item_id}")
# async def get_user_item(
#     user_id: str, item_id: str, q: str | None = None, short: bool = False
# ):
#     item = {"item_id": item_id, "owner_id": user_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item


# # creating a Model class for Item
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# @app.post("/items/{item_id}")
# async def create_item(item: Item) -> Item:  # enforcing the type
#     item_dict = (
#         item.model_dump()
#     )  # can call the model_dump() method on any defined models to convert to dict
#     if item.tax:  # gets the attribute of the class
#         item_dict.update({"price_with_tax": item.price + item.tax})
#     return item_dict


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item, q: str | None = None):
#     result = {"item_id": item_id, **item.model_dump()}
#     if q:
#         result.update({"q": q})
#     return result


# @app.get("/read_items")
# async def read_items(
#     q: str
#     | None = Query(
#         None,
#         min_length=3,
#         max_length=10,
#         title="Query string",
#         description="Query string for the items to search in the database that have a good match",
#         alias="item-query",  # alias is what is used for 'q' in the url
#     )
# ):  # first value is the default (therefore dont need the None |)
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# @app.get("/items_hidden")
# async def hidden_items(hidden_query: str | None = Query(None, include_in_schema=False)):
#     if hidden_query:
#         return {"hidden_query": hidden_query}
#     return {"hidden_query": "Not found"}


# @app.get("/items_validation/{item_id}")
# async def validation_items(
#     item_id: int = Path(
#         ..., title="The ID of the item that we are getting", gt=10, le=100
#     ),
#     q: str = Query("Hello", alias="item-query"),
# ):  # by putting the * as first var it saysthat all following vars are keyword args
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results


"""
Part 7 - Request Body - multiple params
"""


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# class User(BaseModel):
#     username: str
#     full_name: str | None = None


# @app.put("/items/{item_id}")
# async def update_item(
#     *,
#     item_id: int = Path(..., title="The ID of the item to get", ge=0, le=150),
#     q: str | None = None,
#     item: Item | None = None,
#     user: User,
#     importance: int = Body(..., ge=0, le=5)
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     if item:
#         results.update({"item": item})
#     if user:
#         results.update({"user": user})
#     if importance:
#         results.update({"importance": importance})

#     return results


"""
Part 8 - Request Body - fields
"""


# class Item(BaseModel):
#     name: str
#     description: str | None = Field(None, title="The description of the item", max_length=300)
#     price: float = Field(..., gt=0, description="The price must be greater than zero")
#     tax: float | None = None


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item = Body(..., embed=True)):
#     results = {"item_id": item_id, "item": item}
#     return results


"""
Part 9 - Request Body - nested models
"""


# class Image(BaseModel):
#     url: HttpUrl
#     name: str


# class Item(BaseModel):
#     name: str
#     description: str | None = (
#         None  # Field(None, title="The description of the item", max_length=300)
#     )
#     price: float  # = Field(..., gt=0, description="The price must be greater than zero")
#     tax: float | None = None
#     tags: set[str] = set()
#     image: list[Image] | None = None


# class Offer(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     items: list[Item]


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results


# @app.post("/offers/")
# async def create_offer(offer: Offer = Body(..., embed=True)):
#     return offer


# @app.post("/images/multiple/")
# async def create_multiple_images(images: list[Image] = Body(..., embed=True)):
#     return images


"""
Part 10 - Declare Request Example Data
"""


# class Item(BaseModel):
#     name: str  # = Field(..., example="Foo")
#     description: str | None = None  # Field(None, example="A very nice Item")
#     price: float  # = Field(..., example=35.4)
#     tax: float | None = None  # Field(None, example=3.2)


# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: int,
#     item: Item = Body(
#         ...,
#         example={
#             "name": "Foo",
#             "description": "A very nice Item",
#             "price": 35.4,
#             "tax": 3.2,
#         },
#     ),
# ):
#     results = {"item_id": item_id, "item": item}
#     return results


"""
Part 11 - Extra Data Types
"""


# @app.put("/items/{item_id}")
# async def read_items(
#     item_id: UUID,
#     start_date: datetime | None = Body(None),
#     end_date: datetime | None = Body(None),
#     repeat_at: time | None = Body(None),
#     process_after: timedelta | None = Body(None),
# ):
#     start_process = start_date + process_after
#     duration = end_date - start_process
#     return {
#         "item_id": item_id,
#         "start_date": start_date,
#         "repeat_at": repeat_at,
#         "process_after": process_after,
#         "start_process": start_process,
#         "duration": duration,
#     }


"""
Part 12 - Cookie and Header Prams
"""


@app.get("/items/")
async def read_items(
    cookie_id: str | None = Cookie(None),
    accept_encoding: str | None = Header(None, convert_underscores=False),
    sec_ch_ua: str | None = Header(None),
    user_agent: str | None = Header(None),
    x_token: list[str] | None = Header(None),
):
    return {
        "cookie_id": cookie_id,
        "Accept-Encoding": accept_encoding,
        "sec-ch-ua": sec_ch_ua,
        "User-Agent": user_agent,
        "x_token": x_token,
    }
