from pydantic import BaseModel, Field


class SPaymentTransaction(BaseModel):
    transaction_id: str = Field(..., description="Уникальный идентификатор транзакции  в сторонней системе")


class SPayment(SPaymentTransaction):
    account_id: int = Field(..., description="Уникальный идентификатор счета пользователя")
    user_id: int = Field(..., description="Уникальный идентификатор счета пользователя")
    amount: float = Field(..., description="Сумма пополнения счета пользователя")


class SPaymentADD(SPaymentTransaction):
    amount: float = Field(..., description="Сумма пополнения счета пользователя")
    account_id: int = Field(..., description="Уникальный идентификатор счета пользователя")


class SPaymentSignature(SPayment):
    signature: str = Field(..., description="Подпись объекта")
