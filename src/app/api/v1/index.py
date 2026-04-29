from app.core import router


@router.get("/")
async def welcome():
    return "welcome to the inventory api!"
