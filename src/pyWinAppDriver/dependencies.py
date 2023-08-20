import ctypes
import re

from lxml import etree
from pywinauto.controls.uia_controls import UIAElementInfo
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.uia_defines import NoPatternInterfaceError

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW


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


ORIENTATION_TYPE = {
    0: "None",
    1: "Horizontal",
    2: "Vertical",
}

WINDOW_INTERACTION_STATE = {
    0: "Running",
    1: "Closing",
    2: "ReadyForUserInteraction",
    3: "BlockedByModalWindow",
    4: "NotResponding",
}

WINDOW_VISUAL_STATE = {
    0: "Normal",
    1: "Maximized",
    2: "Minimized",
}


def xml_escape(text: str) -> str:
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&apos;")
    return text


def page_source(hwnd: int):
    def convert_iface_value(key, value):
        types = {
            # iface_expanded_collapse
            "ExpandCollapseState": bool,
            # iface_grid
            "ColumnCount": None,
            "RowCount": None,
            # iface_grid_item
            "Column": None,
            "ColumnSpan": None,
            "ContainingGrid": None,
            "Row": None,
            "RowSpan": None,
            # iface_range_value
            "IsReadOnly": bool,
            "LargeChange": None,
            "Maximum": None,
            "Minimum": None,
            "SmallChange": None,
            "Value": None,
            # iface_selection
            "CanSelectMultiple": bool,
            "IsSelectionRequired": bool,
            # iface_selection_item
            "IsSelected": bool,
            "SelectionContainer": None,  # todo {?, ClassName, RuntimeId}
            # iface_scroll
            "HorizontalScrollPercent": None,
            "HorizontalViewSize": None,
            "HorizontallyScrollable": bool,
            "VerticalScrollPercent": None,
            "VerticalViewSize": None,
            "VerticallyScrollable": bool,
            # iface_table
            "RowOrColumnMajor": None,
            # iface_text
            "DocumentRange": None,
            "SupportedTextSelection": bool,
            # iface_toggle
            "ToggleState": bool,
            # iface_transform
            "CanMove": bool,
            "CanResize": bool,
            "CanRotate": bool,
            # iface_transform2
            "CanZoom": bool,
            "ZoomLevel": None,
            "ZoomMaximum": None,
            "ZoomMinimum": None,
            # iface_value
            # "IsReadOnly": bool,
            # "Value": None,
            # iface_window
            "CanMaximize": bool,
            "CanMinimize": bool,
            "IsModal": bool,
            "IsTopmost": bool,
            "WindowInteractionState": lambda x: WINDOW_INTERACTION_STATE[x],
            "WindowVisualState": lambda x: WINDOW_VISUAL_STATE[x],
        }
        fn = types.get(key)
        if fn is None:
            return value
        return fn(value)

    def iter_elements(ctrl):
        control_type = ctrl.element_info.control_type
        attributes = {
            "AutomationId": ctrl.automation_id(),
            "ClassName": ctrl.class_name(),
            "IsEnabled": ctrl.is_enabled(),
            "IsKeyboardFocusable": ctrl.is_keyboard_focusable(),
            "HasKeyboardFocus": ctrl.has_keyboard_focus(),
            "Name": ctrl.window_text(),
            "RuntimeId": ".".join(map(str, ctrl.element_info.runtime_id)),
            "height": ctrl.rectangle().height(),  # todo
            "width": ctrl.rectangle().width(),  # todo
            "x": ctrl.rectangle().left,  # todo
            "y": ctrl.rectangle().top,  # todo
            "IsAvailable": ctrl.is_enabled(),  # Is this correct?
        }
        element_attributes = (
            "AcceleratorKey",
            "AccessKey",
            "FrameworkId",
            "HasKeyboardFocus",
            "HelpText",
            "IsContentElement",
            "IsControlElement",
            "IsEnabled",
            "IsKeyboardFocusable",
            "IsOffscreen",
            "IsPassword",
            "IsRequiredForForm",
            "ItemStatus",
            "ItemType",
            "Localized_ControlType",
            "Orientation",
            "ProcessId",
        )
        # _ needs casting

        for attr in element_attributes:
            try:
                val = getattr(ctrl.element_info.element, f"Current{attr}")
                if any(attr.startswith(prefix) for prefix in ("Has", "Is", "Can")):
                    val = bool(val)
                if attr == "Orientation":
                    val = ORIENTATION_TYPE[val]
                attributes[attr] = val
            except:
                pass

        ifaces = []
        for iface in [attr for attr in dir(ctrl) if attr.startswith("iface_")]:
            try:
                ifaces.append(getattr(ctrl, iface))
            except NoPatternInterfaceError:
                pass
        for iface in ifaces:
            for current_attr in [attr for attr in dir(iface) if attr.startswith("Current")]:
                val = getattr(iface, current_attr)
                attr = current_attr.replace("Current", "")
                attributes[attr] = convert_iface_value(attr, val)

        attributes = {key: attributes[key] for key in sorted(attributes)}

        nonlocal xml_string
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
    iter_elements(top_level_window)
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


if __name__ == "__main__":
    # app = Application(backend="uia").connect(title="電卓", timeout=10)
    # hwnd = app.windows()[0]
    hwnd = 0x1E03EA

    # root = UIAWrapper(UIAElementInfo(hwnd))
    # for i in root.descendants():
    #     print(i)

    ret = page_source(hwnd)
    print(ret)
