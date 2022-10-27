from typing import Union

import uvicorn
from fastapi import FastAPI

import cfw

cfw.run()
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
