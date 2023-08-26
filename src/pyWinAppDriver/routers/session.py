import uuid
from typing import List, Optional

import win32api
from fastapi import APIRouter
from pydantic import BaseModel
from pywinappdriver.dependencies import find_elements_from_page_source, find_window_handle_by_regex, page_source
from pywinappdriver.mouse import click_back_button, click_forward_button
from pywinappdriver.routers import element, touch, window
from pywinappdriver.session_manager import SessionManager
from pywinappdriver.utils import execute_powershell_script, image_to_base64
from pywinauto import Application, mouse
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.uia_element_info import UIAElementInfo

router = APIRouter()

router.include_router(element.router, prefix="/{session_id}/element")
router.include_router(touch.router, prefix="/{session_id}/touch")
router.include_router(window.router, prefix="/{session_id}/window")


class Capabilities(BaseModel):
    platformName: str
    appium_appTopLevelWindow: Optional[str] = None


class DesiredCapabilities(BaseModel):
    platformName: str
    app: Optional[str] = None
    appTopLevelWindow: Optional[str] = None
    # additional
    appTopLevelWindowTitle: Optional[str] = None


class FirstMatch(BaseModel):
    firstMatch: List[Capabilities]


class Session(BaseModel):
    capabilities: FirstMatch
    desiredCapabilities: DesiredCapabilities


@router.post("")
def new_session(data: Session):
    """https://www.w3.org/TR/webdriver/#dfn-new-sessions"""
    caps = data.desiredCapabilities
    platform_name = caps.platformName.lower()
    if platform_name != "windows":
        raise Exception
    app = caps.app
    app_top_level_window = caps.appTopLevelWindow
    app_top_level_window_title = caps.appTopLevelWindowTitle
    value = {"platformName": platform_name}
    if app:
        if app.lower() == "root":
            pass  # todo
        raise Exception
    elif app_top_level_window:
        hwnd = app_top_level_window
        value.update({"appTopLevelWindow": hwnd})
    elif app_top_level_window_title:
        hwnd = hex(find_window_handle_by_regex(app_top_level_window_title))
        value.update({"appTopLevelWindowTitle": hwnd})
    else:
        raise Exception
    session_id = str(uuid.uuid4())
    SessionManager.insert(session_id, caps, UIAWrapper(UIAElementInfo(int(hwnd, 0))))
    return {"sessionId": session_id, "status": 0, "value": value}


@router.get("/{session_id}")
def session(session_id: str):
    caps = SessionManager.select(session_id)
    return {"status": 0, "value": caps}


@router.delete("/{session_id}")
def delete_session(session_id: str):
    SessionManager.delete(session_id)
    return {"status": 0}


@router.get("/{session_id}/source")
def get_page_source(session_id):
    """https://www.w3.org/TR/webdriver/#dfn-get-page-source"""
    root = SessionManager.select(session_id).root
    value = page_source(root.handle)
    return {"sessionId": session_id, "status": 0, "value": value}


@router.post("/{session_id}/back")
def back(session_id: str):
    """https://www.w3.org/TR/webdriver/#dfn-back"""
    click_back_button()
    return {"sessionId": session_id, "status": 0}


@router.post("/{session_id}/forward")
def forward(session_id: str):
    """https://www.w3.org/TR/webdriver/#dfn-forward"""
    click_forward_button()
    return {"sessionId": session_id, "status": 0}


@router.post("/{session_id}/buttondown")
def button_down():
    raise Exception


@router.post("/{session_id}/buttonup")
def button_up():
    raise Exception


@router.post("/{session_id}/click")
def click(session_id: str):
    mouse.click("left")
    return {"sessionId": session_id, "status": 0}


@router.post("/{session_id}/doubleclick")
def double_click(session_id: str):
    mouse.double_click("left")
    return {"sessionId": session_id, "status": 0}


class FindElement(BaseModel):
    using: str
    value: str
    sessionId: str


@router.post("/{session_id}/elements")
def find_elements(session_id: str, data: FindElement):
    """https://www.w3.org/TR/webdriver/#dfn-find-elements"""
    root = SessionManager.select(session_id).root
    elements = find_elements_from_page_source(root, data.using, data.value)
    value = []
    for el in elements:
        value.append({"ELEMENT": el.get("RuntimeId")})
    return {"sessionId": data.sessionId, "status": 0, "value": value}


@router.post("/{session_id}/keys")
def keys():
    raise Exception


@router.get("/{session_id}/location")
def location():
    raise Exception  # server error


@router.post("/{session_id}/moveto")
def move_to_element():
    raise Exception


@router.get("/{session_id}/orientation")
def orientation(session_id: str):  # todo
    return {"sessionId": session_id, "status": 0, "value": "LANDSCAPE"}


@router.get("/{session_id}/screenshot")
def take_screenshot(session_id: str):
    """https://www.w3.org/TR/webdriver/#dfn-take-screenshot"""
    img = SessionManager.select(session_id).root.capture_as_image()
    img_str = image_to_base64(img)
    return {"sessionId": session_id, "status": 0, "value": img_str}


class SetTimeouts(BaseModel):
    pageLoad: int


@router.post("/{session_id}/timeouts")
def set_timeouts(session_id: str, data: SetTimeouts):  # todo
    """https://www.w3.org/TR/webdriver/#dfn-set-timeouts"""
    return {"sessionId": session_id, "status": 0}


@router.get("/{session_id}/title")
def title(session_id: str):  # todo
    return {"sessionId": session_id, "status": 0, "value": "dist"}


@router.get("/{session_id}/window_handle")
def get_window_handle(session_id: str):
    hwnd = SessionManager.select(session_id).window_handle
    return {"sessionId": session_id, "status": 0, "value": hwnd}


@router.get("/{session_id}/window_handles")
def get_window_handles(session_id: str):  # todo unrelated handles for the same process is also obtained
    """https://www.w3.org/TR/webdriver/#dfn-get-window-handles"""
    pid = SessionManager.select(session_id).root.process_id()
    app = Application().connect(process=pid)
    visible_windows = [win for win in app.windows() if win.is_visible() and win.window_text()]
    handles = [hex(win.handle) for win in visible_windows]
    return {"sessionId": session_id, "status": 0, "value": handles}


class ExecuteScript(BaseModel):
    script: str
    args: List[str]


@router.post("/{session_id}/execute")
def execute_script(session_id: str, data: ExecuteScript):
    """Execute PowerShell script"""
    execute_powershell_script(data.script, *data.args)
    return {"sessionId": session_id, "status": 0}


@router.post("/{session_id}/execute/sync")
def execute_sync_script():
    """https://www.w3.org/TR/webdriver/#dfn-execute-script"""
    raise Exception


@router.post("/{session_id}/execute/async")
def execute_async_script():
    """https://www.w3.org/TR/webdriver/#dfn-execute-async-script"""
    raise Exception


@router.post("/{session_id}/frame")
def switch_to_frame():  # switch_to.context
    raise Exception


@router.post("/{session_id}/frame/parent")
def switch_to_parent_frame():
    raise Exception


@router.post("/{session_id}/appium/app/launch")
def launch_app():  # todo
    win32api.WinExec("notepad.exe")


@router.post("/{session_id}/appium/app/close")
def close_app():
    raise Exception
