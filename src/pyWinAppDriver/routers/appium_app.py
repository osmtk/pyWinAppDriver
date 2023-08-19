import win32api
from fastapi import APIRouter

router = APIRouter()  # /session/:sessionId/appium/app


@router.post("/launch")
def launch_app():
    win32api.WinExec("notepad.exe")


@router.post("/close")
def close_app():
    raise Exception
