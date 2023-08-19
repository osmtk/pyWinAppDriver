from fastapi import APIRouter
from pydantic import BaseModel
from pyWinAppDriver.dependencies import find_elements
from pyWinAppDriver.session_manager import SessionManager
from pyWinAppDriver.routers import elementId

router = APIRouter()

router.include_router(elementId.router, prefix="{id}")


class FindElement(BaseModel):
    using: str
    value: str
    sessionId: str


@router.post("")
def find_element(session_id: str, data: FindElement):
    root = SessionManager.select(session_id)
    elements = find_elements(root, data.using, data.value)
    element = elements[0]
    runtime_id = element.get("RuntimeId")
    return {"sessionId": data.sessionId, "status": 0, "value": {"ELEMENT": runtime_id}}


@router.post("/active")
def active():
    raise Exception
