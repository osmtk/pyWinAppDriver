from fastapi import APIRouter
from pywinauto.controls.uia_controls import UIAElementInfo
from pywinauto.controls.uiawrapper import UIAWrapper

from pyWinAppDriver.var import Variable

router = APIRouter()


@router.delete("")
def delete_window():
    raise Exception


@router.post("")
def post_window():
    raise Exception


@router.post("/maximize")
def maximize(session_id: str):
    hwnd = Variable.active_session[session_id]
    UIAWrapper(UIAElementInfo(int(hwnd, 0))).maximize()
    return


@router.post("/minimize")
def minimize(session_id: str):  # additional
    hwnd = Variable.active_session[session_id]
    UIAWrapper(UIAElementInfo(int(hwnd, 0))).minimize()
    return


@router.post("/size")
def window_size():
    raise Exception


@router.get("/size")
def get_window_size():
    raise Exception


@router.post("/{window_handle}/size")
def window_size():
    raise Exception


@router.get("/{window_handle}/size")
def window_size():
    raise Exception


@router.post("/{window_handle}/position")
def window_position():
    raise Exception


@router.get("/{window_handle}/position")
def window_position():
    raise Exception


@router.get("/{window_handle}/maximize")
def maximize(session_id: str, window_handle: str):
    UIAWrapper(UIAElementInfo(int(window_handle, 0))).maximize()
    return


@router.get("/{window_handle}/minimize")
def minimize(session_id: str, window_handle: str):  # additional
    UIAWrapper(UIAElementInfo(int(window_handle, 0))).minimize()
    return


@router.get("/current/position")
def current_windows_position():  # no docs
    raise Exception
