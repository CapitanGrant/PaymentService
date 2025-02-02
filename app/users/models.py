from sqlalchemy import text, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.account.models import Account
from app.dao.database import Base

class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    phone_number: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str]

    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_super_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    account: Mapped['Account'] = relationship("Account", back_populates="user", uselist=False, lazy="joined")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
