from sqlalchemy import Integer, ForeignKey, Float

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.database import Base
from app.payment.models import Payment


class Account(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    balance: Mapped[float] = mapped_column(Float, default=0, nullable=False)

    payment: Mapped[list['Payment']] = relationship("Payment", back_populates="account",cascade="all, delete-orphan")
    user: Mapped['User'] = relationship("User", back_populates="account")

    def __str__(self):
        return f"Account(id={self.id}, user_id={self.user_id}, balance={self.balance})"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "balance": float(self.balance)
        }
