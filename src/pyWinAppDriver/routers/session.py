
import uuid
from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel
from pyWinAppDriver.routers import session_id
from pyWinAppDriver.var import Variable
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.uia_element_info import UIAElementInfo


class Capabilities(BaseModel):
    platformName: str
    appium_appTopLevelWindow: Optional[str] = None


class DesiredCapabilities(BaseModel):
    platformName: str
    app: Optional[str] = None
    appTopLevelWindow: Optional[str] = None


class FirstMatch(BaseModel):
    firstMatch: List[Capabilities]


class Session(BaseModel):
    capabilities: FirstMatch
    desiredCapabilities: DesiredCapabilities


router = APIRouter()
router.include_router(session_id.router, prefix="/{session_id}")


@router.post("")
def start_session(data: Session):
    caps = data.desiredCapabilities
    platform_name = caps.platformName.lower()
    if platform_name != "windows":
        raise Exception
    app = caps.app
    app_top_level_window = caps.appTopLevelWindow
    if app and app_top_level_window:
        raise Exception
    if app:
        raise Exception
    else:
        value = {"appTopLevelWindow": app_top_level_window, "platformName": platform_name}
    session_id = str(uuid.uuid4())
    Variable.active_session[session_id] = UIAWrapper(UIAElementInfo(int(app_top_level_window, 0)))
    return {"sessionId": session_id, "status": 0, "value": value}
