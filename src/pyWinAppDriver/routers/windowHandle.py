from fastapi import APIRouter
from pywinauto.controls.uia_controls import UIAElementInfo
from pywinauto.controls.uiawrapper import UIAWrapper

router = APIRouter()


@router.post("/size")
def window_size():
    raise Exception


@router.get("/size")
def window_size(session_id: str, window_handle: str):
    return {"sessionId": session_id,"status":0,"value":{"height":634,"width":918}}


@router.post("/position")
def window_position():
    raise Exception


@router.get("/position")
def window_position(session_id: str, window_handle: str):
    return {"sessionId": session_id,"status":0,"value":{"x":103,"y":1451}}


@router.post("/maximize")
def maximize(session_id: str, window_handle: str):
    UIAWrapper(UIAElementInfo(int(window_handle, 0))).maximize()


@router.post("/minimize")
def minimize(session_id: str, window_handle: str):  # additional
    UIAWrapper(UIAElementInfo(int(window_handle, 0))).minimize()
