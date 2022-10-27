from typing import Union

import uvicorn
from fastapi import FastAPI

import cfw

cfw.start()
app = FastAPI()


@app.get("/restart")
def read_root():
    return {"Hello": "World"}
