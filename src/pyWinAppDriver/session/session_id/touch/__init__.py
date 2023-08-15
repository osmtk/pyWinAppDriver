from fastapi import APIRouter

router = APIRouter()


@router.post("/click")
def click():
    raise Exception


@router.post("/doubleclick")
def double_click():
    raise Exception


@router.post("/down")
def down():
    raise Exception


@router.post("/flick")
def flick():
    raise Exception


@router.post("/longclick")
def long_click():
    raise Exception


@router.post("/move")
def move():
    raise Exception


@router.post("/scroll")
def scroll():
    raise Exception


@router.post("/up")
def up():
    raise Exception
