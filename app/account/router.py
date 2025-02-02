from fastapi import APIRouter, Depends

from app.users.auth import get_current_user
from app.users.models import User

router = APIRouter(prefix='/account', tags=['Auth'])


@router.get("/all_accounts_and_balances/")
async def get_all_accounts(user_data: User = Depends(get_current_user)):
    pass



