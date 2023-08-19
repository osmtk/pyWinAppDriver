from typing import List, Optional

from pydantic import BaseModel
from pywinauto.controls.uia_controls import UIAElementInfo
from pywinauto.controls.uiawrapper import UIAWrapper
from pyWinAppDriver.dependencies import get_page_source

if __name__ == "__main__":
    # app = Application(backend="uia").connect(title="電卓", timeout=10)
    # main_win = app.windows()[0]
    hwnd = 0xc035a
    ret = get_page_source(hwnd)
    print(ret)
