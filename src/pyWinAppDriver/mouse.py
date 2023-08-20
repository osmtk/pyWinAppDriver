"""https://learn.microsoft.com/ja-jp/windows/win32/api/winuser/nf-winuser-mouse_event"""
import ctypes

INPUT_MOUSE = 0

MOUSEEVENTF_XDOWN = 0x0080
MOUSEEVENTF_XUP = 0x0100


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong), ("wParamL", ctypes.c_short), ("wParamH", ctypes.c_ushort)]


class _INPUT(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT), ("hi", HARDWAREINPUT)]


class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", _INPUT)]


def click_mouse_xbutton(x: int) -> None:
    xbutton_down = INPUT(type=INPUT_MOUSE, ii=_INPUT(mi=MOUSEINPUT(mouseData=x, dwFlags=MOUSEEVENTF_XDOWN)))
    xbutton_up = INPUT(type=INPUT_MOUSE, ii=_INPUT(mi=MOUSEINPUT(mouseData=x, dwFlags=MOUSEEVENTF_XUP)))

    ctypes.windll.user32.SendInput(1, ctypes.byref(xbutton_down), ctypes.sizeof(xbutton_down))
    ctypes.windll.user32.SendInput(1, ctypes.byref(xbutton_up), ctypes.sizeof(xbutton_up))


def click_back_button() -> None:
    click_mouse_xbutton(1)


def click_forward_button() -> None:
    click_mouse_xbutton(2)
