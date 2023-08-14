import uuid

import uvicorn
import win32api
import win32gui
from fastapi import FastAPI
from win32.lib import win32con

from pywinauto.controls.uia_controls import UIAElementInfo

from pywinauto.controls.uiawrapper import UIAWrapper
from endpoint.session.session_id.source import get_page_source
from endpoint.session import Session

app = FastAPI()

active_session = {}





@app.post("/session")
def open(session: Session):
    caps = session.desiredCapabilities
    device_name = caps.deviceName
    platform_name = caps.platformName.lower()
    if platform_name != "windows":
        raise Exception
    app = caps.app
    app_top_level_window = caps.appTopLevelWindow
    if app and app_top_level_window:
        status = -1
    elif app:
        status = -1  # open app
    elif app_top_level_window:
        status = 0
    else:
        status = -1
    value = {"appTopLevelWindow": app_top_level_window, "platformName": platform_name}

    session_id = str(uuid.uuid4())
    global active_session
    active_session[session_id] = app_top_level_window
    return {"sessionId": session_id, "status": status, "value": value}


@app.delete("/session/{session_id}")
def close(session_id: str):
    try:
        del active_session[session_id]
    except KeyError:
        pass
    return {"status": 0}


@app.post("/session/{session_id}/appium/app/launch")
def launch_app():
    win32api.WinExec("notepad.exe")
    return


@app.get("/session/{session_id}/source")
def source(session_id):
    status = 0
    global active_session
    hwnd = active_session[session_id]
    value = get_page_source(int(hwnd, 0))
    return {"sessionId": session_id, "status": status, "value": value}


@app.post("/session/{session_id}/window/maximize")
def maximize(session_id: str):
    global active_session
    hwnd = active_session[session_id]
    UIAWrapper(UIAElementInfo(int(hwnd, 0))).maximize()
    return


@app.post("/session/{session_id}/window/minimize")
def minimize(session_id: str):  # additional
    global active_session
    hwnd = active_session[session_id]
    UIAWrapper(UIAElementInfo(int(hwnd, 0))).minimize()
    return


@app.get("/session/{session_id}/window/{window_handle}/maximize")
def maximize(session_id: str, window_handle: str):
    UIAWrapper(UIAElementInfo(int(window_handle, 0))).maximize()
    return


@app.get("/session/{session_id}/window/{window_handle}/minimize")
def minimize(session_id: str, window_handle: str):  # additional
    UIAWrapper(UIAElementInfo(int(window_handle, 0))).minimize()
    return


@app.get("/session/{session_id}/window_handle")
def window_handle(session_id: str):
    # hwnd = hex(win32gui.FindWindow("Notepad", None))  # class name?
    # window_title = ""
    # hwnd = hex(win32gui.FindWindow(None, window_title))
    global active_session
    return active_session[session_id]


@app.get("/status")
def status():
    return


@app.get("/sessions")
def sessions():
    return


@app.post("/session/{session_id}/appium/app/close")
def close_app():
    return


@app.post("/session/{session_id}/back")
def back():
    return


@app.post("/session/{session_id}/buttondown")
def button_down():
    return


@app.post("/session/{session_id}/buttonup")
def button_up():
    return


@app.post("/session/{session_id}/click")
def click():
    return


@app.post("/session/{session_id}/doubleclick")
def double_click():
    return


@app.post("/session/{session_id}/element")
def element():
    return


@app.post("/session/{session_id}/elements")
def elements():
    return


@app.post("/session/{session_id}/element/active")
def active():
    return


@app.get("/session/{session_id}/element/{id}/attribute/{name}")
def get_attribute():
    return


@app.post("/session/{session_id}/element/{id}/clear")
def clear():
    return


@app.post("/session/{session_id}/element/{id}/click")
def click_element():
    return


@app.get("/session/{session_id}/element/{id}/displayed")
def displayed():
    return


@app.get("/session/{session_id}/element/{id}/element")
def get_element():
    return


@app.get("/session/{session_id}/element/{id}/elements")
def get_elements():
    return


@app.get("/session/{session_id}/element/{id}/enabled")
def enabled():
    return


@app.get("/session/{session_id}/element/{id}/equals")
def equals():
    return


@app.get("/session/{session_id}/element/{id}/location")
def location():
    return


@app.get("/session/{session_id}/element/{id}/location_in_view")
def location_in_view():
    return


@app.get("/session/{session_id}/element/{id}/name")
def name():
    return


@app.get("/session/{session_id}/element/{id}/screenshot")
def screenshot():
    return


@app.get("/session/{session_id}/element/{id}/selected")
def selected():
    return


@app.get("/session/{session_id}/element/{id}/size")
def size():
    return


@app.get("/session/{session_id}/element/{id}/text")
def text():
    return


@app.post("/session/{session_id}/element/{id}/value")
def value():
    return


@app.post("/session/{session_id}/forward")
def forward():
    return


@app.post("/session/{session_id}/keys")
def keys():
    return


@app.get("/session/{session_id}/location")
def location():
    return


@app.post("/session/{session_id}/moveto")
def move_to_element():
    return


@app.get("/session/{session_id}/orientation")
def orientation():
    return


@app.get("/session/{session_id}/screenshot")
def screenshot():
    return


@app.post("/session/{session_id}/timeouts")
def timeouts():
    return


@app.get("/session/{session_id}/title")
def title():
    return


@app.post("/session/{session_id}/touch/click")
def click():
    return


@app.post("/session/{session_id}/touch/doubleclick")
def double_click():
    return


@app.post("/session/{session_id}/touch/down")
def down():
    return


@app.post("/session/{session_id}/touch/flick")
def flick():
    return


@app.post("/session/{session_id}/touch/longclick")
def long_click():
    return


@app.post("/session/{session_id}/touch/move")
def move():
    return


@app.post("/session/{session_id}/touch/scroll")
def scroll():
    return


@app.post("/session/{session_id}/touch/up")
def up():
    return


@app.delete("/session/{session_id}/window")
def delete_window():
    return


@app.post("/session/{session_id}/window")
def post_window():
    return


@app.post("/session/{session_id}/window/size")
def window_size():
    return


@app.post("/session/{session_id}/window/size")
def get_window_size():
    return


@app.post("/session/{session_id}/window/{window_handle}/size")
def window_size():
    return


@app.get("/session/{session_id}/window/{window_handle}/size")
def window_size():
    return


@app.post("/session/{session_id}/window/{window_handle}/position")
def window_position():
    return


@app.get("/session/{session_id}/window/{window_handle}/position")
def window_position():
    return


@app.get("/session/{session_id}/window_handles")
def window_handles():
    return


@app.get("/session/{session_id}/window/current/position")
def current_windows_position():  # no docs
    return


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
