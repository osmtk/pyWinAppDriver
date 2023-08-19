
import uuid
from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel
from pyWinAppDriver.dependencies import find_window_handle_by_regex
from pyWinAppDriver.routers import sessionId
from pyWinAppDriver.session_manager import SessionManager
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.uia_element_info import UIAElementInfo


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


router = APIRouter()
router.include_router(sessionId.router, prefix="/{session_id}")


@router.post("")
def start_session(data: Session):
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
            pass
        raise Exception
    elif app_top_level_window:
        hwnd = app_top_level_window
        if isinstance(hwnd, str):
            hwnd = int(hwnd, 0)
        value.update({"appTopLevelWindow": hwnd})
    elif app_top_level_window_title:
        hwnd = find_window_handle_by_regex(app_top_level_window_title)
        value.update({"appTopLevelWindowTitle": hwnd})
    else:
        raise Exception
    session_id = str(uuid.uuid4())
    SessionManager.insert(session_id, caps, UIAWrapper(UIAElementInfo(hwnd)))
    return {"sessionId": session_id, "status": 0, "value": value}
