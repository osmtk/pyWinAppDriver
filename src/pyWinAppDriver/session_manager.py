from dataclasses import dataclass
from typing import Dict

from pywinauto.controls.uiawrapper import UIAWrapper


@dataclass()
class Session:
    session_id: str
    capabilities: dict
    root: UIAWrapper

    @property
    def window_handle(self):
        return self.root.handle


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
