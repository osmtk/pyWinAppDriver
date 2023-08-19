from fastapi import APIRouter
from pyWinAppDriver.routers import windowHandle
from pyWinAppDriver.session_manager import SessionManager
from pywinauto.controls.uia_controls import UIAElementInfo
from pywinauto.controls.uiawrapper import UIAWrapper

router = APIRouter()

router.include_router(windowHandle.router, prefix="{window_handle")


@router.delete("")
def delete_window():
    raise Exception


@router.post("")
def post_window():
    raise Exception


@router.post("/maximize")
def maximize(session_id: str):
    root = SessionManager.select(session_id)
    UIAWrapper(UIAElementInfo(root.handle)).maximize()


@router.post("/minimize")
def minimize(session_id: str):  # additional
    root = SessionManager.select(session_id)
    UIAWrapper(UIAElementInfo(root.handle)).minimize()


@router.post("/size")
def window_size():
    raise Exception


@router.get("/size")
def get_window_size(session_id: str):
    raise {"sessionId": session_id,"status":0,"value":{"height":634,"width":918}}


@router.get("/current/position")
def current_windows_position(session_id: str):  # no docs
    return {"sessionId": session_id,"status":0,"value":{"x":103,"y":1451}}
