from dataclasses import dataclass
from pywinauto.controls.uiawrapper import UIAWrapper


@dataclass()
class Session:

    session_id: str
    capabilities: dict
    root_control: UIAWrapper

    @property
    def window_handle(self):
        return


class SessionManager:

    _session = {}

    @classmethod
    def insert(cls, session_id, capabilities, root_control):
        if session_id in cls._session:
            raise ValueError("Key already exists!")
        cls._session[session_id] = Session(session_id, capabilities, root_control)

    @classmethod
    def select(cls, key):
        return cls._session.get(key, None)

    @classmethod
    def delete(cls, key):
        if key in cls._session:
            del cls._session[key]
