from typing import List, Optional

from pydantic import BaseModel


class Capabilities(BaseModel):
    deviceName: str
    platformName: str
    app: Optional[str] = None
    appTopLevelWindow: Optional[str] = None


class FirstMatch(BaseModel):
    firstMatch: List[Capabilities]


class Session(BaseModel):
    capabilities: FirstMatch
    desiredCapabilities: Capabilities
