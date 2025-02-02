from sqlalchemy import Integer, String, ForeignKey, Float

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.database import Base


class Payment(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    transaction_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)

    account: Mapped['Account'] = relationship("Account",
                                               back_populates="payment", uselist=False)


    def __str__(self):
        return f"Payment(id={self.id}, transaction_id={self.transaction_id}, user_id={self.user_id}, account_id={self.account_id}, amount={self.amount}, created_at={self.created_at})"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "user_id": self.user_id,
            "account_id": self.account_id,
            "amount": float(self.amount)
        }
