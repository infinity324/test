from fastapi import FastAPI, Path, BackgroundTasks
from typing import Annotated, Literal
from pydantic import BaseModel, Field
from enum import Enum
from re import T
import time
import asyncio

app = FastAPI(debug=True)


@app.get("/sleep")
async def sleep_example():
    await asyncio.sleep(3)  # 不阻塞线程
    return {"message": "Slept asynchronously!"}


async def tem():
    await asyncio.sleep(3)  # 不阻塞线程


def main():
    asyncio.run(tem())  # 阻塞线程
    print("Done!")


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


# @app.get("/items/")
# async def read_items(filter_query: FilterParams):
#     return filter_query


# @app.get("/items/{item_id}")
# async def read_items(
#     item_id: Annotated[int, Path(title="The ID of the item to get")],
#     q: Annotated[str | None, Query(alias="item-query")] = None,
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item, q: str | None = None):
#     result = {"item_id": item_id, **item.dict()}
#     if q:
#         result.update({"q": q})
#     return result


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/nihao")
async def nihao():
    return {"message": "nihao"}


@app.get("/hello")
async def hello(background_tasks: BackgroundTasks):
    def loop_hello():
        while True:
            print("Hello World")
            time.sleep(1)

    background_tasks.add_task(loop_hello)
    return {"message": "Started background task"}


@app.get("/task")
async def task():
    cnt = 10
    while cnt > 0:
        print("Task is running")
        await asyncio.sleep(1)  # ✅ 这是非阻塞的睡眠
        cnt -= 1
    return {"message": "Task is done"}
