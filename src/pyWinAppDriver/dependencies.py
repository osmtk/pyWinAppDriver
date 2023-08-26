import ctypes
import re
from typing import Any, Dict

from lxml import etree
from pywinappdriver.property_identifiers import (
    AUTOMATION_ELEMENT_PROPIDS,
    CONTROL_PATTERN_PROPIDS,
    CONTROL_TYPE,
    DOCK_POSITION,
    EXPAND_COLLAPSE_STATE,
    ORIENTATION_TYPE,
    TOGGLE_STATE,
    WINDOW_INTERACTION_STATE,
    WINDOW_VISUAL_STATE,
    lcid_to_locale_name,
)
from pywinauto.controls.uia_controls import UIAElementInfo
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.uia_defines import NoPatternInterfaceError

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW


def ms_compatible_sort(props) -> Dict[str, Any]:
    order = []
    order.extend(AUTOMATION_ELEMENT_PROPIDS)
    order.extend(["x", "y", "width", "height"])
    order.extend(CONTROL_PATTERN_PROPIDS)
    order.extend(["IsAvailable"])
    sorted_props = {key: props.get(key) for key in order}
    sorted_props.update(props)
    return sorted_props


def get_attribute(control: UIAWrapper, name: str):
    return get_attributes(control).get(name)


def get_attributes(control: UIAWrapper, origin=(0, 0)):
    def get_value_for_win_app_driver(ctrl, trim_margin: bool) -> Dict[str, Any]:
        window_margin = 7 if trim_margin else 0  # todo Is this constant?
        return {
            "x": ctrl.rectangle().left + window_margin - origin[0],
            "y": ctrl.rectangle().top - origin[1],
            "height": ctrl.rectangle().height() - window_margin,
            "width": ctrl.rectangle().width() - window_margin * 2,
        }

    def get_element_value(ctrl) -> Dict[str, Any]:
        values = {}
        for attr in AUTOMATION_ELEMENT_PROPIDS:
            try:
                values[attr] = getattr(ctrl.element_info.element, f"Current{attr}")
            except AttributeError:
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
            if i == "iface_selection":
                values["Selection"] = iface.GetCurrentSelection()
            for current_key in [a for a in dir(iface) if a.startswith("Current")]:
                value = getattr(iface, current_key)
                key = current_key.replace("Current", "")
                values[key] = value
        return values

    def is_available(props):
        """Whether there is a value to get from the control pattern property. (for compatibility with WinAppDriver)"""
        for k in props:
            if k in CONTROL_PATTERN_PROPIDS:
                return True
        return None

    def convert_type(key: str, value: Any):
        def get_iui_automation_element(element):
            try:
                name = element.CurrentName
            except ValueError:
                name = ""
            try:
                class_name = element.CurrentClassName
            except ValueError:
                class_name = ""
            try:
                runtime_id = element.GetRuntimeId()
            except ValueError:
                runtime_id = ()
            el = f"{{{name}, {class_name}, {runtime_id_to_str(runtime_id)}}}"
            if el == "{, , }":
                return None
            return el

        def get_iui_automation_element_array(element_array):
            length = int(element_array.Length)
            if length:
                array = []
                for i in range(length):
                    try:
                        runtime_id = element_array.GetElement(i).GetRuntimeId()
                    except ValueError:
                        runtime_id = ()
                    array.append(runtime_id)
                if any(array):
                    return ", ".join(map(runtime_id_to_str, array))
            return None

        def get_rect(rect):
            if any([rect.left, rect.top, rect.right, rect.bottom]):
                return f"{{l:{rect.left} t:{rect.top} r:{rect.right} b:{rect.bottom}}}"
            return None

        if any(key.startswith(prefix) for prefix in ("Can", "Has", "Is", "Supported")):
            return bool(value)
        if key.endswith("Scrollable"):
            return bool(value)
        if key in ("HorizontalScrollPercent", "VerticalScrollPercent", "HorizontalViewSize", "VerticalViewSize"):
            return int(value)
        if key == "RuntimeId":
            return ".".join(map(str, value))
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
        if key in ("ContainingGrid", "SelectionContainer", "LabeledBy"):
            return get_iui_automation_element(value)
        if key in ("ControllerFor", "DescribedBy", "Selection"):
            return get_iui_automation_element_array(value)
        if key in "BoundingRectangle":
            return get_rect(value)
        if key == "ControlType":
            return CONTROL_TYPE[value]
        if key == "Culture":
            return lcid_to_locale_name(value)
        if key == "Selection":
            return value  # todo retrieve this
        return value

    attributes = {}
    attributes.update(get_element_value(control))
    attributes.update({"RuntimeId": control.element_info.runtime_id})
    attributes.update(get_iface_value(control))
    attributes.update(get_value_for_win_app_driver(control, bool(attributes.get("CanResize"))))
    attributes = {k: convert_type(k, attributes[k]) for k in attributes}
    if attributes["ControlType"] != "Custom":
        attributes.update({"IsAvailable": is_available(attributes)})
    attributes = ms_compatible_sort(attributes)  # todo temp
    return {k: v for k, v in attributes.items() if v is not None}


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


def runtime_id_tuple_to_str(runtime_id):
    return ".".join(map(str, runtime_id))


def page_source(hwnd: int):
    def iter_elements(ctrl, top_level: bool = False):
        nonlocal xml_string
        nonlocal origin
        attributes = get_attributes(ctrl, origin)
        if top_level:
            origin = (attributes["x"], attributes["y"])
            attributes["x"], attributes["y"] = 0, 0

        control_type = attributes["ControlType"]
        xml_string += f"<{control_type}"
        for attr, val in attributes.items():
            xml_string += f' {attr}="{xml_escape(str(val))}"'
        if ctrl.children():
            xml_string += ">"
            for child in ctrl.children():
                iter_elements(child)
            xml_string += f"</{control_type}>"
        else:
            xml_string += " />"

    top_level_window = UIAWrapper(UIAElementInfo(hwnd))
    xml_string = '<?xml version="1.0" encoding="utf-16"?>'
    origin = (0, 0)
    iter_elements(top_level_window, top_level=True)
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


def runtime_id_to_str(runtime_id):
    return ".".join(map(str, runtime_id))


def runtime_id_from_str(id: str):
    return tuple(map(int, id.split(".")))
