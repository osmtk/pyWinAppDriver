import ctypes


# Automation element property
# CULTURE
def lcid_to_locale_name(lcid: int) -> str:
    locale_name_max_length = 85
    buf = ctypes.create_unicode_buffer(locale_name_max_length)
    result = ctypes.windll.kernel32.LCIDToLocaleName(lcid, buf, locale_name_max_length, 0)
    if result:
        return buf.value
    return ''


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
