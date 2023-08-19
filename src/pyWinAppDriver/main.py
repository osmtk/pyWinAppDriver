import uvicorn
from fastapi import FastAPI
from pyWinAppDriver.routers import session

app = FastAPI()


@app.get("/status")
def status():
    return {
        "build": {
            "revision": "18001",
            "time": "Tue Sep 18 18:35:38 2018",
            "version": "1.1.1809",
        },
        "os": {
            "arch": "amd64",
            "name": "windows",
            "version": "10.0.19045",
        },
    }


app.include_router(session.router, prefix="/session")


@app.get("/sessions")
def sessions():
    return {
        "status": 0,
        "value": [
            {
                "capabilities": {
                    "appTopLevelWindow": "0x205d0",
                    "platformName": "Windows",
                },
                "id": "A18DD7C6-F8B8-4333-A538-616544F47CE1",
            },
        ],
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
