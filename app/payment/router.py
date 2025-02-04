import hashlib
import os

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from app.account.dao import AccountsDAO
from app.account.schemas import SAccountID, SAccountCreate, SAccountBalance
from app.dao.session_maker import SessionDep, TransactionSessionDep
from app.payment.dao import PaymentsDAO
from app.users.auth import get_current_user
from app.users.dao import UsersDAO
from app.users.models import User

from app.payment.schemas import SPaymentTransaction, SPayment, SPaymentSignature, SPaymentADD

router = APIRouter(prefix="/payment", tags=["Payments"])

SECRET_KEY = os.getenv("SECRET_KEY_SIGNATURE_1")


def verify_signature(data: SPaymentSignature) -> bool:
    expected_string = f"{data.account_id}{data.amount}{data.transaction_id}{data.user_id}{SECRET_KEY}"
    print(f"VERIFY STRING: '{expected_string}'")
    expected_signature = hashlib.sha256(expected_string.encode("utf-8")).hexdigest()
    print(f"VERIFY SIGNATURE: {expected_signature}")
    return expected_signature == data.signature


def create_payload():
    payload = {
        "transaction_id": "16",
        "account_id": 4,
        "user_id": 1,
        "amount": 11.0,
    }
    expected_string = f"{payload['account_id']}{payload['amount']}{payload['transaction_id']}{payload['user_id']}{SECRET_KEY}"
    print(f"CREATE STRING: '{expected_string}'")
    expected_signature = hashlib.sha256(expected_string.encode("utf-8")).hexdigest()
    print(f"CREATE SIGNATURE: {expected_signature}")
    return expected_signature


print(create_payload())


@router.get("/all/", summary='Получить список всех своих платежей')
async def get_all_payments(user_data: User = Depends(get_current_user), session: AsyncSession = SessionDep):
    return await PaymentsDAO.find_all(session=session, filters=None)


@router.post("/webhook/")
async def webhook(payload: SPaymentSignature, session: AsyncSession = TransactionSessionDep):
    try:

        if not verify_signature(payload):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid signature')

        transaction_id = payload.transaction_id
        account_id = payload.account_id
        amount = payload.amount
        user_id = payload.user_id
        find_user_id = await UsersDAO.find_one_or_none_by_id(session=session, data_id=user_id)
        if not find_user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        find_transaction_id = await PaymentsDAO.find_one_or_none(session=session, filters=SPaymentTransaction(
            transaction_id=transaction_id))
        if find_transaction_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Payment already processed')

        find_account_id = await AccountsDAO.find_one_or_none(session=session, filters=SAccountID(id=account_id))
        if not find_account_id:
            await AccountsDAO.add(session=session, values=SAccountCreate(user_id=user_id, balance=amount))
        current_amount = await AccountsDAO.find_one_or_none(session=session, filters=SAccountID(id=account_id))
        update_balance = current_amount.balance + amount
        await PaymentsDAO.add(session=session,
                              values=SPaymentADD(transaction_id=transaction_id, account_id=account_id, amount=amount))
        await AccountsDAO.update(session=session, values=SAccountBalance(balance=update_balance),
                                 filters=SAccountID(id=account_id))
    except HTTPException as e:
        logger.error(e)
        raise e
