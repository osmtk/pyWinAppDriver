from fastapi import APIRouter
from pydantic import BaseModel

from pyWinAppDriver.util import find_elements, find_element_by_runtime_id, convert_runtime_id
from pyWinAppDriver.var import Variable

router = APIRouter()


class FindElement(BaseModel):
    using: str
    value: str
    sessionId: str


@router.post("")
def find_element(session_id: str, data: FindElement):
    root = Variable.active_session[session_id]
    elements = find_elements(root, data.using, data.value)
    element = elements[0]
    runtime_id = element.get("RuntimeId")
    return {"sessionId": data.sessionId, "status": 0, "value": {"ELEMENT": runtime_id}}


@router.post("/active")
def active():
    raise Exception


@router.get("/{id}/attribute/{name}")
def get_attribute():
    raise Exception


@router.post("/{id}/clear")
def clear():
    raise Exception


@router.post("/{id}/click")
def click_element(session_id: str, id: str):
    root = Variable.active_session[session_id]
    runtime_id = convert_runtime_id(id)
    element = find_element_by_runtime_id(root, runtime_id)
    element.click_input()
    return {"sessionId": session_id, "status": 0}


@router.get("/{id}/displayed")
def displayed():
    raise Exception


@router.get("/{id}/element")
def get_element(session_id: str, id: str, data: FindElement):
    root = Variable.active_session[session_id]
    context = find_element_by_runtime_id(root, convert_runtime_id(id))
    elements = find_elements(context, data.using, data.value)
    element = elements[0]
    runtime_id = element.get("RuntimeId")
    return {"sessionId": data.sessionId, "status": 0, "value": {"ELEMENT": runtime_id}}


@router.get("/{id}/elements")
def get_elements(session_id: str, id: str, data: FindElement):
    root = Variable.active_session[session_id]
    context = find_element_by_runtime_id(root, convert_runtime_id(id))
    elements = find_elements(context, data.using, data.value)
    value = []
    for element in elements:
        value.append({"ELEMENT": element.get("RuntimeId")})
    return {"sessionId": data.sessionId, "status": 0, "value": value}


@router.get("/{id}/enabled")
def enabled():
    raise Exception


@router.get("/{id}/equals")
def equals():
    raise Exception


@router.get("/{id}/location")
def location():
    raise Exception


@router.get("/{id}/location_in_view")
def location_in_view():
    raise Exception


@router.get("/{id}/name")
def name():
    raise Exception


@router.get("/{id}/screenshot")
def screenshot():
    raise Exception


@router.get("/{id}/selected")
def selected():
    raise Exception


@router.get("/{id}/size")
def size():
    raise Exception


@router.get("/{id}/text")
def text(session_id: str, id: str):
    root = Variable.active_session[session_id]
    element = find_element_by_runtime_id(root, convert_runtime_id(id))
    return {"sessionId": session_id, "status": 0, "value": element.window_text()}


@router.post("/{id}/value")
def value():
    raise Exception
