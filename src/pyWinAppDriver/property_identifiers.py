import ctypes


# Automation element property
# CULTURE
def lcid_to_locale_name(lcid: int) -> str:
    locale_name_max_length = 85
    buf = ctypes.create_unicode_buffer(locale_name_max_length)
    result = ctypes.windll.kernel32.LCIDToLocaleName(lcid, buf, locale_name_max_length, 0)
    if result:
        return buf.value
    return ""


AUTOMATION_ELEMENT_PROPIDS = (
    "AcceleratorKey",
    "AccessKey",
    "AnnotationObjects",
    "AnnotationTypes",
    "AriaProperties",
    "AriaRole",
    "AutomationId",
    "BoundingRectangle",
    "CenterPoint",
    "ClassName",
    "ClickablePoint",
    "ControllerFor",
    "ControlType",
    "Culture",
    "DescribedBy",
    "FillColor",
    "FillType",
    "FlowsFrom"
    "FlowsTo",
    "FrameworkId",
    "FullDescription",
    "HasKeyboardFocus",
    "HeadingLevel",
    "HelpText",
    "IsContentElement",
    "IsControlElement",
    "IsDataValidForForm",
    "IsDialog",
    "IsEnabled",
    "IsKeyboardFocusable",
    "IsOffscreen",
    "IsPassword",
    "IsPeripheral",
    "IsRequiredForForm",
    "ItemStatus",
    "ItemType",
    "LabeledBy",
    "LandmarkType",
    "Level",
    "LiveSetting",
    "LocalizedControlType",
    "LocalizedLandmarkType",
    "Name",
    "NativeWindowHandle",
    "OptimizeForVisualContent",
    "Orientation",
    "OutlineColor",
    "OutlineThickness",
    "PositionInSet",
    "ProcessId",
    "ProviderDescription"
    "Rotation",
    "RuntimeId",
    "Size",
    "SizeOfSet",
    "VisualEffects",
)

CONTROL_TYPE = control_types = {
    50000: "Button",
    50001: "Calendar",
    50002: "CheckBox",
    50003: "ComboBox",
    50004: "Edit",
    50005: "Hyperlink",
    50006: "Image",
    50007: "ListItem",
    50008: "List",
    50009: "Menu",
    50010: "MenuBar",
    50011: "MenuItem",
    50012: "ProgressBar",
    50013: "RadioButton",
    50014: "ScrollBar",
    50015: "Slider",
    50016: "Spinner",
    50017: "StatusBar",
    50018: "Tab",
    50019: "TabItem",
    50020: "Text",
    50021: "ToolBar",
    50022: "ToolTip",
    50023: "Tree",
    50024: "TreeItem",
    50025: "Custom",
    50026: "Group",
    50027: "Thumb",
    50028: "DataGrid",
    50029: "DataItem",
    50030: "Document",
    50031: "SplitButton",
    50032: "Window",
    50033: "Pane",
    50034: "Header",
    50035: "HeaderItem",
    50036: "Table",
    50037: "TitleBar",
    50038: "Separator",
    50039: "SemanticZoom",
    50040: "AppBar"
}


ORIENTATION_TYPE = {
    0: "None",
    1: "Horizontal",
    2: "Vertical",
}

# Control pattern property
DOCK_POSITION = {
    0: "Top",
    1: "Left",
    2: "Bottom",
    3: "Right",
    4: "Fill",
    5: "None",
}

EXPAND_COLLAPSE_STATE = {
    0: "Collapsed",
    1: "Expanded",
    2: "PartiallyExpanded",
    3: "LeafNode",
}

TOGGLE_STATE = {
    0: "Off",
    1: "On",
    2: "Indeterminate",
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
