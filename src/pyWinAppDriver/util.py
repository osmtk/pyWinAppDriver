from lxml import etree
from pywinauto.controls.uia_controls import UIAElementInfo
from pywinauto.controls.uiawrapper import UIAWrapper


def get_page_source(hwnd: int):

    def iter_elements(ctrl):
        uia_elem = UIAElementInfo(ctrl.handle)

        attributes = {
            'AutomationId': ctrl.automation_id(),
            "ClassName": ctrl.class_name(),
            'IsEnabled': ctrl.is_enabled(),
            'IsKeyboardFocusable': ctrl.is_keyboard_focusable(),
            'HasKeyboardFocus': ctrl.has_keyboard_focus(),
            "Name": ctrl.window_text(),
            "RuntimeId": ".".join(map(str, ctrl.element_info.runtime_id)),  # todo
            "height": ctrl.rectangle().height(),  # todo
            "width": ctrl.rectangle().width(),  # todo
            "x": ctrl.rectangle().left,  # todo
            "y": ctrl.rectangle().top,  # todo
            "IsAvailable": "",  # todo
        }

        def convert_to_tag(friendly_class_name):
            if friendly_class_name == "Dialog":
                return "Window"
            if friendly_class_name == "Menu":
                return "MenuBar"
            if friendly_class_name == "MenuItem":
                return "MenuItem"
            if friendly_class_name == "Button":
                return "Button"
            if friendly_class_name == "Static":
                return "Text"
            if friendly_class_name == "Custom":
                return "Custom"
            if friendly_class_name == "GroupBox":
                return "Group"
            if friendly_class_name == "TabControl":
                return "Tab"
            return friendly_class_name

        tag = convert_to_tag(ctrl.friendly_class_name())

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
            "NativeWindowHandle",
            "Orientation",
            "ProcessId",
        )
        # _ needs casting
        additional_element_attributes = (
            "AriaProperties",
            "AriaRole",
            "_BoundingRectangle",
            "_ControlType",
            "_ControllerFor",
            "Culture",
            "_DescribedBy",
            "_FlowsTo",
            "IsDataValidForForm",
            "_LabeledBy",
            "_ProvidedDescription",
        )

        for attr in element_attributes:
            try:
                val = getattr(uia_elem.element, f"Current{attr}")
                if any(attr.startswith(prefix) for prefix in ("Has", "Is", "Can")):
                    val = bool(val)
                if attr == "Orientation" and not val:
                    val = None
                attributes[attr] = val
            except:
                pass

        try:
            window = ctrl.iface_window
            window_interaction_state = {
                2: "ReadyForUserInteraction",
            }
            window_visual_state = {
                0: "Normal",
            }
            window_attr = {
                "CanMaximize": str(bool(window.CurrentCanMaximize)),
                "CanMinimize": str(bool(window.CurrentCanMinimize)),
                "IsModal": str(bool(window.CurrentIsModal)),
                "IsTopmost": str(bool(window.CurrentIsTopmost)),
                "WindowInteractionState": window_interaction_state[window.CurrentWindowInteractionState],
                "WindowVisualState": window_visual_state[window.CurrentWindowVisualState],
            }
            attributes.update(window_attr)
        except:
            pass

        try:
            transform = ctrl.iface_transform
            transform_attr = {
                "CanMove": str(bool(transform.CurrentCanMove)),
                "CanResize": str(bool(transform.CurrentCanResize)),
                "CanRotate": str(bool(transform.CurrentCanRotate)),
            }
            attributes.update(transform_attr)
        except:
            pass

        try:
            scroll = ctrl.iface_scroll
            scroll_attr = {
                "HorizontalScrollPercent": scroll.CurrentHorizontalScrollPercent,
                "HorizontalViewSize": scroll.CurrentHorizontalViewSize,
                "HorizontallyScrollable": str(bool(scroll.CurrentHorizontallyScrollable)),
                "VerticalScrollPercent": scroll.CurrentVerticalScrollPercent,
                "VerticalViewSize": scroll.CurrentVerticalViewSize,
                "VerticallyScrollable": str(bool(scroll.CurrentVerticallyScrollable)),
            }
            attributes.update(scroll_attr)
        except:
            pass

        attributes = {key: attributes[key] for key in sorted(attributes)}

        nonlocal xml_string
        xml_string += f'<{tag} '
        for attr, val in attributes.items():
            xml_string += f'{attr}="{val}" '

        if ctrl.children():
            xml_string += '>'
            for child in ctrl.children():
                iter_elements(child)
            xml_string += f'</{tag}>'
        else:
            xml_string += '/>'

    top_level_window = UIAWrapper(UIAElementInfo(hwnd))
    xml_string = '<?xml version="1.0" encoding="utf-16"?>'
    iter_elements(top_level_window)  # todo top_level_window.descendants()
    return xml_string


def find_element_by_runtime_id(root: UIAWrapper, runtime_id) -> UIAWrapper:
    if root.element_info.runtime_id == runtime_id:
        return root
    for child in root.descendants():
        if child.element_info.runtime_id == runtime_id:
            return child
    raise Exception


def find_elements(root: UIAWrapper, using: str, value: str):
    page_source = get_page_source(root.handle)
    root = etree.fromstring(page_source.encode("utf16"))
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
    hwnd = 0x1e03ea
    ret = get_page_source(hwnd)
    print(ret)
