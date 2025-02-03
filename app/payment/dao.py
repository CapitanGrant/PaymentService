from app.dao.base import BaseDAO
from app.payment.models import Payment


class PaymentsDAO(BaseDAO):
    model = Payment
