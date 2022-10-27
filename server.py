import uvicorn

from fastapi import FastAPI

import cfw

app = FastAPI()


@app.get("/restart")
def read_root():
    cfw.restart()
    return {"code": 1}


if __name__ == "__main__":
    cfw.start()
    uvicorn.run("server:app", port=cfw.config["port"])
