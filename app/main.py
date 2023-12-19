from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from result import Result
import logging
from aip import AipImageClassify
from pymongo import MongoClient

app = FastAPI()
result = Result()

APP_ID = '44767258'
API_KEY = 'PCotYmhuxzkPnsOR9yucTsg8'
SECRET_KEY = '7UI6k2eeH7yBeS9EWARkwyfaUGtrG7Mu'
client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
logger.addHandler(ch)

mongodb = MongoClient("mongodb://60.204.219.4:27017")
db = mongodb["pocket_go"]
collection = db["user_item"]


class Request(BaseModel):
    user_id: int
    item_name: str


# Result: {code: , message:{}, data: }
@app.get("/test")
async def root():
    return result.success()


@app.post("/plant_detect")
async def plantDetect(file: UploadFile = File(...)):

    image = await file.read()
    res = client.plantDetect(image)

    return result.success(res)


@app.post("/animal_detect")
async def animalDetect(file: UploadFile = File(...)):

    image = await file.read()
    res = client.animalDetect(image)

    return result.success(res)


@app.post("/fruit_detect")
async def fruitDetect(file: UploadFile = File(...)):

    image = await file.read()
    res = client.ingredient(image)

    return result.success(res)


@app.post("/item_pickup")
def item_pickup(item: Request):
    query_result = collection.update_one(
        {"_id": item.user_id},
        {"$inc": {item.item_name: 1}}
    )
    return result.success(query_result.raw_result)


@app.post("/item_list")
async def item_list(user_id: int):
    query_result = collection.find({"_id": user_id})
    for data in query_result:
        print(data)
        return result.success(data)
