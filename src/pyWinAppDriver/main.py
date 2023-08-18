import uvicorn
from fastapi import FastAPI
from pyWinAppDriver.routers import session

app = FastAPI()


@app.get("/status")
def status():
    raise Exception


app.include_router(session.router, prefix="/session")


@app.get("/sessions")
def sessions():
    raise Exception


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
