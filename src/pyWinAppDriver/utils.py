import base64
import ctypes
import subprocess
from io import BytesIO
from typing import TypedDict


class SystemMetrics(TypedDict):
    frame_width: int
    frame_height: int
    margin_width: int
    margin_height: int
    border_width: int
    border_height: int


def image_to_base64(image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode("utf-8")


def execute_powershell_script(script: str, *args: str) -> str:
    """Execute PowerShell script"""
    cmd = ["powershell", "-Command", script] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return result.stdout.rstrip()


def get_system_metrics() -> SystemMetrics:  # todo
    ctypes.windll.user32.SetProcessDPIAware()
    system_metrics = ctypes.windll.user32.GetSystemMetrics
    border_width = system_metrics(5)  # SM_CXBORDER
    border_height = system_metrics(6)  # SM_CYBORDER
    # frame_width = system_metrics(32)  # SM_CXFRAME
    # frame_height = system_metrics(33)  # SM_CYFRAME
    frame_width = 8
    frame_height = 8
    return SystemMetrics(
        frame_width=frame_width,
        frame_height=frame_height,
        margin_width=frame_width - border_width,
        margin_height=frame_height - border_height,
        border_width=border_width,
        border_height=border_height,
    )
