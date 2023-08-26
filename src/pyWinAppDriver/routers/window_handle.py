from fastapi import APIRouter
from pydantic import BaseModel
from pywinappdriver.utils import get_system_metrics
from pywinauto.controls.hwndwrapper import HwndWrapper
from pywinauto.controls.uia_controls import UIAElementInfo

router = APIRouter()


def __get_window(hwnd: str) -> HwndWrapper:
    return HwndWrapper(UIAElementInfo(int(hwnd, 0)))


class SetWindowSize(BaseModel):
    width: int
    height: int


@router.post("/size")
def set_window_size(session_id: str, window_handle: str, data: SetWindowSize):
    __get_window(window_handle).move_window(width=data.width, height=data.height)
    return {"sessionId": session_id, "status": 0}


@router.get("/size")
def get_window_size(session_id: str, window_handle: str):
    window = __get_window(window_handle)
    metrics = get_system_metrics()
    return {
        "sessionId": session_id,
        "status": 0,
        "value": {
            "height": window.client_rect().height() + metrics["border_height"],
            "width": window.client_rect().width() + metrics["border_width"] * 2,
        },
    }


class SetWindowPosition(BaseModel):
    x: int
    y: int


@router.post("/position")
def set_window_position(session_id: str, window_handle: str, data: SetWindowPosition):
    __get_window(window_handle).move_window(x=data.x, y=data.y)
    return {"sessionId": session_id, "status": 0}


@router.get("/position")
def get_window_position(session_id: str, window_handle: str):
    element = __get_window(window_handle)
    metrics = get_system_metrics()
    return {
        "sessionId": session_id,
        "status": 0,
        "value": {
            "x": element.rectangle().left + metrics["frame_width"] - metrics["border_width"],
            "y": element.rectangle().top,
        },
    }


@router.post("/maximize")
def maximize(session_id: str, window_handle: str):
    __get_window(window_handle).maximize()
    return {"sessionId": session_id, "status": 0}


@router.post("/minimize")
def minimize(session_id: str, window_handle: str):  # additional
    __get_window(window_handle).minimize()
    return {"sessionId": session_id, "status": 0}
