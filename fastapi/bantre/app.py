from typing import Optional

from fastapi import FastAPI
from sqlmodel import SQLModel

from bantre.database import create_db_and_tables
from bantre.modules.routes import v1_router


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(v1_router, prefix="/v1")


# Below is boilerplate code
class Item(SQLModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def get_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
