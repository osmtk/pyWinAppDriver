import uvicorn
from fastapi import FastAPI

from pyWinAppDriver.root import router as root_router

app = FastAPI()
app.include_router(root_router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
