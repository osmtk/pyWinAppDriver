from fastapi import APIRouter
from pydantic import BaseModel
from pywinappdriver.routers import window_handle
from pywinappdriver.session_manager import SessionManager
from pywinappdriver.utils import get_system_metrics
from pywinauto.controls.hwndwrapper import HwndWrapper
from pywinauto.controls.uia_controls import UIAElementInfo

router = APIRouter()


def __get_window(session_id: str) -> HwndWrapper:
    hwnd = SessionManager.select(session_id).window_handle
    hwnd = int(hwnd, 0)
    return HwndWrapper(UIAElementInfo(hwnd))


@router.get("")
def get_window_handle(session_id: str):
    """https://www.w3.org/TR/webdriver/#dfn-get-window-handle"""
    SessionManager.select(session_id).window_handle
    raise Exception


@router.delete("")
def close_window():
    """https://www.w3.org/TR/webdriver/#dfn-close-window"""
    raise Exception


@router.post("")
def switch_to_window():
    """https://www.w3.org/TR/webdriver/#dfn-switch-to-window"""
    raise Exception


@router.post("/current/maximize")
def maximize_current_window(session_id: str):
    __get_window(session_id).maximize()
    return {"sessionId": session_id, "status": 0}


@router.post("/current/maximize")
def maximize_window(session_id: str):
    """https://www.w3.org/TR/webdriver/#dfn-maximize-window"""
    __get_window(session_id).maximize()
    return {"sessionId": session_id, "status": 0}


@router.post("/minimize")
def minimize_window(session_id: str):
    """https://www.w3.org/TR/webdriver/#dfn-minimize-window"""
    __get_window(session_id).minimize()
    return {"sessionId": session_id, "status": 0}


class SetWindowSize(BaseModel):
    width: int
    height: int


@router.post("/size")
def window_size(session_id: str, data: SetWindowSize):
    window = __get_window(session_id)
    window.move_window(width=data.width, height=data.height)
    return {"sessionId": session_id, "status": 0}


@router.get("/size")
def get_window_size(session_id: str):
    window = __get_window(session_id)
    metrics = get_system_metrics()
    return {
        "sessionId": session_id,
        "status": 0,
        "value": {
            "height": window.client_rect().height() + metrics["border_height"],
            "width": window.client_rect().width() + metrics["border_width"] * 2,
        },
    }


@router.get("/current/position")
def current_windows_position(session_id: str):  # no docs
    window = __get_window(session_id)
    metrics = get_system_metrics()
    return {
        "sessionId": session_id,
        "status": 0,
        "value": {
            "x": window.rectangle().left + metrics["frame_width"] - metrics["border_width"],
            "y": window.rectangle().top,
        },
    }


@router.get("/rect")
def get_window_rect(session_id: str):
    """https://www.w3.org/TR/webdriver/#dfn-get-window-rect"""
    window = __get_window(session_id)
    metrics = get_system_metrics()
    return {
        "sessionId": session_id,
        "status": 0,
        "value": {
            "x": window.rectangle().left + metrics["frame_width"] - metrics["border_width"],
            "y": window.rectangle().top,
            "height": window.client_rect().height() + metrics["border_height"],
            "width": window.client_rect().width() + metrics["border_width"] * 2,
        },
    }


class SetWindowRect(BaseModel):
    x: int
    y: int
    width: int
    height: int


@router.post("/rect")
def set_window_rect(session_id: str, data: SetWindowRect):
    """https://www.w3.org/TR/webdriver/#dfn-set-window-rect"""
    __get_window(session_id).move_window(x=data.x, y=data.y, width=data.width, height=data.height)
    return {"sessionId": session_id, "status": 0}


router.include_router(window_handle.router, prefix="/{window_handle}")
