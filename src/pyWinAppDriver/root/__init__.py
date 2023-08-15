from fastapi import APIRouter

from pyWinAppDriver.root.session import router as session_router

router = APIRouter()


@router.get("/status")
def status():
    raise Exception


router.include_router(session_router, prefix="/session")


@router.get("/sessions")
def sessions():
    raise Exception
