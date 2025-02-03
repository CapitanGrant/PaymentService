from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.session_maker import SessionDep, TransactionSessionDep
from app.users.auth import get_current_user
from app.users.models import User
from app.account.dao import AccountsDAO
from app.account.schemas import SAccountBase, SAccountCreate

# uvicorn app.main:app --port 8001

router = APIRouter(prefix='/account', tags=['Счета'])


@router.get("/all_accounts_and_balances/")
async def get_all_accounts(user_data: User = Depends(get_current_user), session: AsyncSession = SessionDep):
    result = await AccountsDAO.find_all(session=session, filters=None)
    return [{'id': i.id, 'balance': i.balance} for i in result]


@router.post("/new_account/", summary='Создать новый счет, с указанным балансом')
async def new_account(value_balance: SAccountBase, user_data: User = Depends(get_current_user),
                      session: AsyncSession = TransactionSessionDep):
    update_balance = value_balance.model_dump()
    updated_balance = {'user_id': user_data.id, **update_balance}
    return await AccountsDAO.add(session=session, values=SAccountCreate(**updated_balance))
