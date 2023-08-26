import json

import uvicorn
from fastapi import FastAPI
from pywinappdriver.routers import session
from pywinappdriver.session_manager import SessionManager
from pywinappdriver.utils import execute_powershell_script

app = FastAPI()


@app.get("/status")
def status():
    """
    https://www.w3.org/TR/webdriver/#status
    """
    os_info_script = """
    $arch = if ([Environment]::Is64BitOperatingSystem) { "amd64" } else { "x86" }
    $osInfo = @{
        arch = $arch
        name = "windows"
        version = (Get-CimInstance Win32_OperatingSystem).Version
    }
    $osInfo | ConvertTo-Json
    """
    os_info = json.loads(execute_powershell_script(os_info_script))
    return {
        "build": {  # todo
            "revision": "1",
            "time": "Sub Dec 31 12:00:0 2023",
            "version": "0.1.0",
        },
        "os": os_info,
    }


@app.get("/sessions")
def sessions():
    return {
        "status": 0,
        "value": SessionManager.all_sessions(),
    }


app.include_router(session.router, prefix="/session")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
