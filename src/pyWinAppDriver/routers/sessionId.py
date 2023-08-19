import win32api
from fastapi import APIRouter
from pyWinAppDriver.dependencies import find_elements, get_page_source
from pyWinAppDriver.routers import appium_app, element, touch, window
from pyWinAppDriver.session_manager import SessionManager

from .element import FindElement

router = APIRouter()

router.include_router(appium_app.router, prefix="/appium/app")
router.include_router(element.router, prefix="/element")
router.include_router(touch.router, prefix="/touch")
router.include_router(window.router, prefix="/window")


@router.get("")
def session(session_id: str):

    return {"status":0,"value":{"appTopLevelWindow":"0x205d0","platformName":"Windows"}}


@router.delete("")
def quit(session_id: str):
    SessionManager.delete(session_id)
    return {"status": 0}


@router.post("/appium/app/launch")
def launch_app():
    win32api.WinExec("notepad.exe")
    return


@router.post("/appium/app/close")
def close_app():
    raise Exception


@router.get("/source")
def page_source(session_id):
    status = 0
    root = SessionManager.select(session_id)
    value = get_page_source(root.handle)
    return {"sessionId": session_id, "status": status, "value": value}


@router.post("/back")
def back():
    raise Exception


@router.post("/buttondown")
def button_down():
    raise Exception


@router.post("/buttonup")
def button_up():
    raise Exception


@router.post("/click")
def click():
    raise Exception


@router.post("/doubleclick")
def double_click():
    raise Exception


@router.post("/elements")
def elements(session_id: str, data: FindElement):
    root = SessionManager.select(session_id)
    elements = find_elements(root, data.using, data.value)
    value = []
    for element in elements:
        value.append({"ELEMENT": element.get("RuntimeId")})
    return {"sessionId": data.sessionId, "status": 0, "value": value}


@router.post("/forward")
def forward():
    raise Exception


@router.post("/keys")
def keys():
    raise Exception


@router.get("/location")
def location():
    raise Exception  # server error


@router.post("/moveto")
def move_to_element():
    raise Exception


@router.get("/orientation")
def orientation(session_id: str):
    return {"sessionId": session_id,"status":0,"value":"LANDSCAPE"}


@router.get("/screenshot")
def screenshot(session_id: str):
    return {"sessionId":session_id,"status":0,"value": "screenshot"}


@router.post("/timeouts")
def timeouts():
    raise Exception


@router.get("/title")
def title(session_id: str):
    return {"sessionId": session_id,"status":0,"value":"dist"}


@router.get("/window_handle")
def window_handle(session_id: str):
    return {"sessionId": session_id,"status":0,"value":"0x000205D0"}


@router.get("/window_handles")
def window_handles(session_id: str):
    raise {"sessionId": session_id,"status":0,"value":["0x000205D0","0x001F0586"]}


@router.post("/execute")
def execute_script():
    raise Exception
