import win32api
from fastapi import APIRouter
from pyWinAppDriver.routers import element, touch, window
from pyWinAppDriver.util import find_elements, get_page_source
from pyWinAppDriver.var import Variable

from .element import FindElement

router = APIRouter()


@router.get("")
def session(session_id: str):
    raise Exception


@router.delete("")
def quit(session_id: str):
    try:
        del Variable.active_session[session_id]
    except KeyError:
        pass
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
    window = Variable.active_session[session_id]
    value = get_page_source(window.handle)
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


router.include_router(element.router, prefix="/element")


@router.post("/elements")
def elements(session_id: str, data: FindElement):
    root = Variable.active_session[session_id]
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
    raise Exception


@router.post("/moveto")
def move_to_element():
    raise Exception


@router.get("/orientation")
def orientation():
    raise Exception


@router.get("/screenshot")
def screenshot():
    raise Exception


@router.post("/timeouts")
def timeouts():
    raise Exception


@router.get("/title")
def title():
    raise Exception


router.include_router(touch.router, prefix="/touch")
router.include_router(window.router, prefix="/window")


@router.get("/window_handle")
def window_handle(session_id: str):
    return Variable.active_session[session_id]


@router.get("/window_handles")
def window_handles():
    raise Exception


@router.post("/execute")
def execute_script():
    raise Exception
