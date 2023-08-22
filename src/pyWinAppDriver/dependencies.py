import ctypes
import re
from typing import Dict, Any

from lxml import etree
from pywinauto.controls.uia_controls import UIAElementInfo
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.uia_defines import NoPatternInterfaceError

from pywinappdriver.property_identifiers import (
    AUTOMATION_ELEMENT_PROPIDS,
    ORIENTATION_TYPE,
    DOCK_POSITION,
    EXPAND_COLLAPSE_STATE,
    TOGGLE_STATE,
    WINDOW_INTERACTION_STATE,
    WINDOW_VISUAL_STATE,
    CONTROL_TYPE,
    lcid_to_locale_name,
)

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW


def get_attribute(control: UIAWrapper, name: str):
    return get_attributes(control).get(name)


def get_attributes(control: UIAWrapper):

    def get_value_for_win_app_driver(ctrl):
        return {
            "height": ctrl.rectangle().height(),  # todo
            "width": ctrl.rectangle().width(),  # todo
            "x": ctrl.rectangle().left,  # todo
            "y": ctrl.rectangle().top,  # todo
            "IsAvailable": ctrl.is_enabled(),  # Is this correct?
        }

    def get_element_value(ctrl) -> Dict[str, Any]:
        values = {}
        for attr in AUTOMATION_ELEMENT_PROPIDS:
            try:
                val = getattr(ctrl.element_info.element, f"Current{attr}")
                if any(attr.startswith(prefix) for prefix in ("Has", "Is", "Can")):
                    val = bool(val)
                if attr == "Orientation":
                    val = ORIENTATION_TYPE[val]
                values[attr] = val
            except:
                continue
        return values

    def get_iface_value(ctrl) -> Dict[str, Any]:
        values = {}
        ifaces = [a for a in dir(ctrl) if a.startswith("iface_")]
        for i in ifaces:
            try:
                iface = getattr(ctrl, i)
            except NoPatternInterfaceError:
                continue
            for current_key in [a for a in dir(iface) if a.startswith("Current")]:
                value = getattr(iface, current_key)
                key = current_key.replace("Current", "")
                values[key] = value
        return values

    def convert_type(key, value):
        if any(key.startswith(prefix) for prefix in ("Can", "Has", "Is", "Supported")):
            return bool(value)
        if key.endswith("Scrollable"):
            return bool(value)
        if key == "Orientation":
            return ORIENTATION_TYPE.get(value)
        if key == "DockPosition":
            return DOCK_POSITION.get(value)
        if key == "ToggleState":
            return TOGGLE_STATE.get(value)
        if key == "WindowInteractionState":
            return WINDOW_INTERACTION_STATE.get(value)
        if key == "WindowVisualState":
            return WINDOW_VISUAL_STATE.get(value)
        if key == "ExpandCollapseState":
            return EXPAND_COLLAPSE_STATE.get(value)
        if key == "SelectionContainer":
            pass  # todo {?, ClassName, RuntimeId}
        # Not supported by WinAppDriver
        if key == "ControlType":
            return CONTROL_TYPE[value]
        if key == "Culture":
            return lcid_to_locale_name(value)
        if key == "ControllerFor":
            pass
        if key == "DescribedBy":
            pass
        if key == "BoundingRectangle":
            pass
        if key == "LabeledBy":
            pass
        return value

    attributes = {}
    attributes.update(get_element_value(control))
    attributes.update(get_value_for_win_app_driver(control))
    attributes.update(get_iface_value(control))
    attributes.update({"RuntimeId": ".".join(map(str, control.element_info.runtime_id))})
    return {k: convert_type(k, attributes[k]) for k in sorted(attributes) if attributes[k] is not None}


def find_window_handle_by_regex(pattern):
    hwnds = []

    def foreach_window(hwnd, lParam):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        if re.match(pattern, buff.value):
            hwnds.append(hwnd)
        return True

    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return hwnds[0] if hwnds else None


def xml_escape(text: str) -> str:
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&apos;")
    return text


def page_source(hwnd: int):

    def iter_elements(ctrl, top_level_window: bool = False):

        nonlocal xml_string
        attributes = get_attributes(ctrl)
        control_type = attributes["ControlType"]
        xml_string += f"<{control_type} "
        for attr, val in attributes.items():
            xml_string += f'{attr}="{xml_escape(str(val))}" '
        if ctrl.children():
            xml_string += ">"
            for child in ctrl.children():
                iter_elements(child)
            xml_string += f"</{control_type}>"
        else:
            xml_string += "/>"

    top_level_window = UIAWrapper(UIAElementInfo(hwnd))
    xml_string = '<?xml version="1.0" encoding="utf-16"?>'
    iter_elements(top_level_window, top_level_window=True)
    return xml_string


def find_element_by_runtime_id(root: UIAWrapper, runtime_id) -> UIAWrapper:
    if root.element_info.runtime_id == runtime_id:
        return root
    for child in root.descendants():
        if child.element_info.runtime_id == runtime_id:
            return child
    raise Exception


def find_elements_from_page_source(root: UIAWrapper, using: str, value: str) -> list:
    root = etree.fromstring(page_source(root.handle).encode("utf16"))
    if using == "id":
        xpath = f'//*[@AutomationId="{value}"]'
    elif using == "accessibility id":
        xpath = f'//*[@AutomationId="{value}"]'
    elif using == "xpath":
        xpath = value
    elif using == "name":
        xpath = f'//*[@Name="{value}"]'
    elif using == "class name":
        xpath = f'//*[@ClassName="{value}"]'
    else:
        raise Exception
    found_elements = root.xpath(xpath)
    if not found_elements:
        raise Exception
    return found_elements


def convert_runtime_id(id: str):
    return tuple(map(int, id.split(".")))
