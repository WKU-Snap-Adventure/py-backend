from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from result import Result
import logging
from aip import AipImageClassify

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


class Request(BaseModel):
    staticFootPrint: list
    dynamicFootPrint: list
    url: str
    bucket_name: str


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
