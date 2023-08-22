from dataclasses import dataclass
from typing import List, TypedDict, Dict, Union

from pywinauto.controls.uiawrapper import UIAWrapper


class SessionDict(TypedDict):
    capabilities: Dict[str, Union[str, int]]
    id: str


@dataclass()
class Session:
    session_id: str
    capabilities: dict
    root: UIAWrapper

    @property
    def window_handle(self):
        return self.root.handle

    def asdict(self) -> SessionDict:
        return SessionDict(
            capabilities=self.capabilities,
            id=self.session_id,
        )


class SessionManager:
    _session: Dict[str, Session] = {}

    @classmethod
    def insert(cls, session_id: str, capabilities, root) -> None:
        if session_id in cls._session:
            raise ValueError("Key already exists!")
        cls._session[session_id] = Session(session_id, capabilities, root)

    @classmethod
    def select(cls, session_id: str) -> Session:
        return cls._session.get(session_id, None)

    @classmethod
    def delete(cls, session_id: str) -> None:
        if session_id in cls._session:
            del cls._session[session_id]

    @classmethod
    def all_sessions(cls) -> List[SessionDict]:
        return [session.asdict() for session in cls._session.values()]
