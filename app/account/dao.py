from app.dao.base import BaseDAO
from app.account.models import Account


class AccountsDAO(BaseDAO):
    model = Account
