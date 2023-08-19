from fastapi import APIRouter
from pydantic import BaseModel
from pyWinAppDriver.dependencies import convert_runtime_id, find_element_by_runtime_id, find_elements
from pyWinAppDriver.session_manager import SessionManager

router = APIRouter()


class FindElement(BaseModel):
    using: str
    value: str
    sessionId: str


@router.get("/attribute/{name}")
def get_attribute(session_id: str, element_id: str, name: str):
    return {"sessionId": session_id,"status":0,"value":"電卓"}


@router.post("/clear")
def clear():
    raise Exception


@router.post("/click")
def click_element(session_id: str, element_id: str):
    root = SessionManager.select(session_id)
    runtime_id = convert_runtime_id(element_id)
    element = find_element_by_runtime_id(root, runtime_id)
    element.click_input()
    return {"sessionId": session_id, "status": 0}


@router.get("/displayed")
def displayed(session_id: str, element_id: str):
    return {"sessionId": session_id, "status": 0, "value": True}


@router.get("/element")
def get_element(session_id: str, element_id: str, data: FindElement):
    root = SessionManager.select(session_id)
    context = find_element_by_runtime_id(root, convert_runtime_id(element_id))
    elements = find_elements(context, data.using, data.value)
    element = elements[0]
    runtime_id = element.get("RuntimeId")
    return {"sessionId": data.sessionId, "status": 0, "value": {"ELEMENT": runtime_id}}


@router.get("/elements")
def get_elements(session_id: str, element_id: str, data: FindElement):
    root = SessionManager.select(session_id)
    context = find_element_by_runtime_id(root, convert_runtime_id(element_id))
    elements = find_elements(context, data.using, data.value)
    value = []
    for element in elements:
        value.append({"ELEMENT": element.get("RuntimeId")})
    return {"sessionId": data.sessionId, "status": 0, "value": value}


@router.get("/enabled")
def enabled(session_id: str, element_id: str):
    return {"sessionId": session_id, "status": 0, "value": True}


@router.get("/equals/{other_id}")
def equals(session_id: str, element_id: str, other_element_id: str):
    is_equal = element_id == other_element_id
    return {"sessionId": session_id, "status": 0, "value": is_equal}


@router.get("/location")
def location(session_id: str, element_id: str):
    return {"sessionId": session_id,"status":0,"value":{"x":-7,"y":0}}


@router.get("/location_in_view")
def location_in_view(session_id: str, element_id: str):
    return {"sessionId": session_id,"status":0,"value":{"x":-7,"y":0}}


@router.get("/name")
def name(session_id: str, element_id: str):
    return {"sessionId": session_id,"status":0,"value":"ControlType.Button"}


@router.get("/screenshot")
def screenshot(session_id: str, element_id: str):
    return {"sessionId": session_id, "status": 0, "value": "screenshot"}


@router.get("/selected")
def selected(session_id: str, element_id: str):
    return {"sessionId": session_id, "status": 0, "value": True}


@router.get("/size")
def size(session_id: str, element_id: str):
    return {"sessionId": session_id, "status": 0, "value":{"height":32,"width":46}}


@router.get("/text")
def text(session_id: str, element_id: str):
    root = SessionManager.select(session_id)
    element = find_element_by_runtime_id(root, convert_runtime_id(element_id))
    return {"sessionId": session_id, "status": 0, "value": element.window_text()}


@router.post("/value")
def value():
    raise Exception
