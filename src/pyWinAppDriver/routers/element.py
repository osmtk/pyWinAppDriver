from fastapi import APIRouter
from pydantic import BaseModel
from pywinappdriver.dependencies import (
    find_element_by_runtime_id,
    find_elements_from_page_source,
    get_attribute,
    runtime_id_from_str,
)
from pywinappdriver.session_manager import SessionManager
from pywinappdriver.utils import image_to_base64
from pywinauto.controls.uiawrapper import UIAWrapper

router = APIRouter()


def __get_element(session_id, element_id) -> UIAWrapper:
    root = SessionManager.select(session_id).root
    return find_element_by_runtime_id(root, runtime_id_from_str(element_id))


class FindElement(BaseModel):
    using: str
    value: str
    sessionId: str


@router.post("")
def find_element(session_id: str, data: FindElement):
    """https://www.w3.org/TR/webdriver/#dfn-find-element"""
    root = SessionManager.select(session_id).root
    elements = find_elements_from_page_source(root, data.using, data.value)
    element = elements[0]
    runtime_id = element.get("RuntimeId")
    return {"sessionId": data.sessionId, "status": 0, "value": {"ELEMENT": runtime_id}}


@router.post("/active")
def active(session_id: str):
    """https://www.w3.org/TR/webdriver/#dfn-get-active-element"""
    return {"sessionId": session_id, "status": 0, "value": {"ELEMENT": "42.1770846"}}


@router.get("/{element_id}/attribute/{name}")
def get_element_attribute(session_id: str, element_id: str, name: str):
    """https://www.w3.org/TR/webdriver/#dfn-get-element-attribute"""
    element = __get_element(session_id, element_id)
    return {"sessionId": session_id, "status": 0, "value": get_attribute(element, name)}


@router.post("/{element_id}/clear")
def element_clear(session_id: str, element_id: str):  # todo
    __get_element(session_id, element_id)
    return {"sessionId": session_id, "status": 0}


@router.post("/{element_id}/click")
def element_click(session_id: str, element_id: str):
    """https://www.w3.org/TR/webdriver/#dfn-element-click"""
    element = __get_element(session_id, element_id)
    element.click_input()
    return {"sessionId": session_id, "status": 0}


@router.get("/{element_id}/displayed")
def is_element_displayed(session_id: str, element_id: str):
    return {"sessionId": session_id, "status": 0, "value": True}


@router.get("/{element_id}/element")
def find_element_from_element(session_id: str, element_id: str, data: FindElement):
    """https://www.w3.org/TR/webdriver/#dfn-find-element-from-element"""
    context = __get_element(session_id, element_id)
    element = find_elements_from_page_source(context, data.using, data.value)[0]
    runtime_id = element.get("RuntimeId")
    return {"sessionId": data.sessionId, "status": 0, "value": {"ELEMENT": runtime_id}}


@router.get("/{element_id}/elements")
def find_elements_from_element(session_id: str, element_id: str, data: FindElement):
    """https://www.w3.org/TR/webdriver/#dfn-find-elements-from-element"""
    context = __get_element(session_id, element_id)
    elements = find_elements_from_page_source(context, data.using, data.value)
    value = []
    for element in elements:
        value.append({"ELEMENT": element.get("RuntimeId")})
    return {"sessionId": data.sessionId, "status": 0, "value": value}


@router.get("/{element_id}/enabled")
def is_element_enabled(session_id: str, element_id: str):  # todo
    """https://www.w3.org/TR/webdriver/#dfn-is-element-enabled"""
    element = __get_element(session_id, element_id)
    return {"sessionId": session_id, "status": 0, "value": element.is_enabled()}


@router.get("/{element_id}/equals/{other_id}")
def equals(session_id: str, element_id: str, other_element_id: str):
    is_equal = element_id == other_element_id
    return {"sessionId": session_id, "status": 0, "value": is_equal}


@router.get("/{element_id}/location")
def element_location(session_id: str, element_id: str):
    element = __get_element(session_id, element_id)
    return {
        "sessionId": session_id,
        "status": 0,
        "value": {
            "x": element.rectangle().left,
            "y": element.rectangle().top,
        },
    }


@router.get("/{element_id}/location_in_view")
def element_location_in_view(session_id: str, element_id: str):  # todo
    element = __get_element(session_id, element_id)
    return {
        "sessionId": session_id,
        "status": 0,
        "value": {
            "x": element.rectangle().left,
            "y": element.rectangle().top,
        },
    }


@router.get("/{element_id}/name")
def get_element_tag_name(session_id: str, element_id: str):
    """https://www.w3.org/TR/webdriver/#dfn-get-element-tag-name"""
    element = __get_element(session_id, element_id)
    control_type = f"ControlType.{element.element_info.control_type}"
    return {"sessionId": session_id, "status": 0, "value": control_type}


@router.get("/{element_id}/screenshot")
def take_element_screenshot(session_id: str, element_id: str):
    """https://www.w3.org/TR/webdriver/#dfn-take-element-screenshot"""
    img = __get_element(session_id, element_id).capture_as_image()
    img_str = image_to_base64(img)
    return {"sessionId": session_id, "status": 0, "value": img_str}


@router.get("/{element_id}/selected")
def is_element_selected(session_id: str, element_id: str):
    """https://www.w3.org/TR/webdriver/#dfn-is-element-selected"""
    element = __get_element(session_id, element_id)
    return {"sessionId": session_id, "status": 0, "value": element.is_selected()}


@router.get("/{element_id}/size")
def size(session_id: str, element_id: str):
    element = __get_element(session_id, element_id)
    return {
        "sessionId": session_id,
        "status": 0,
        "value": {
            "height": int(element.rectangle().height()),
            "width": int(element.rectangle().width()),
        },
    }


@router.get("/{element_id}/text")
def get_element_text(session_id: str, element_id: str):
    """https://www.w3.org/TR/webdriver/#dfn-get-element-text"""
    element = __get_element(session_id, element_id)
    return {"sessionId": session_id, "status": 0, "value": element.window_text()}


@router.post("/{element_id}/value")
def element_send_keys(session_id: str, element_id: str):  # todo
    """https://www.w3.org/TR/webdriver/#dfn-element-send-keys"""
    # {"text": "aaa", "value": ["a", "a", "a"], "id": "42.591676", "sessionId": "1D9B84A2-D0F1-42EA-8EEA-404D376AEA18"}
    __get_element(session_id, element_id)
    return {"sessionId": session_id, "status": 0}
