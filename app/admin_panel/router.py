from fastapi import APIRouter, HTTPException, status, Depends
from app.account.schemas import SAccount
from app.dao.session_maker import TransactionSessionDep, SessionDep
from app.users.auth import get_password_hash, get_current_admin_user
from app.users.dao import UsersDAO
from app.users.models import User
from app.users.schemas import SUserRegister, SUserMail, SUserWithAccounts
from app.dao.database import AsyncSession

router = APIRouter(prefix='/admin', tags=['Admin'])


@router.post("/create_user/")
async def register_user(user_data: SUserRegister, session: AsyncSession = TransactionSessionDep,
                        admin: User = Depends(get_current_admin_user)) -> dict:
    user_filter = SUserMail(email=user_data.email)
    user = await UsersDAO.find_one_or_none(session=session, filters=user_filter)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add(session=session, values=SUserRegister(**user_dict))
    return {'message': 'Вы успешно добавили нового пользователя!'}


@router.put("/update_user/")
async def update_user(user_data: SUserRegister, session: AsyncSession = TransactionSessionDep,
                      admin: User = Depends(get_current_admin_user)):
    user_filter = SUserMail(email=user_data.email)
    user = await UsersDAO.find_one_or_none(session=session, filters=user_filter)
    if user:
        user_dict = user_data.model_dump()
        user_dict['password'] = get_password_hash(user_data.password)
        return await UsersDAO.update(session=session, filters=user_filter, values=SUserRegister(**user_dict))
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователя не существует'
        )


@router.delete("/delete_user/")
async def delete_user(user_data: SUserMail, session: AsyncSession = TransactionSessionDep,
                      admin: User = Depends(get_current_admin_user)):
    user_filter = SUserMail(email=user_data.email)
    user = await UsersDAO.find_one_or_none(session=session, filters=user_filter)
    if user:
        return await UsersDAO.delete(session=session, filters=user_filter)
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователя не существует'
        )


@router.get("/all_user_balance_accounts/")
async def get_all_user_balance_accounts(session: AsyncSession = SessionDep,
                                        admin: User = Depends(get_current_admin_user)):
    users = await UsersDAO.find_all(session=session, filters=None)
    result = []
    for user in users:
        accounts_data = [SAccount(balance=accounts.balance, user_id=accounts.user_id, id=accounts.id) for accounts in
                         user.account]
        user_data = SUserWithAccounts(email=user.email, first_name=user.first_name, last_name=user.last_name,
                                      account=accounts_data)
        result.append(user_data)

    return result
