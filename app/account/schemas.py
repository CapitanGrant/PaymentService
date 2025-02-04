from pydantic import BaseModel, Field


class SAccountBalance(BaseModel):
    balance: float = Field(..., gt=0, description="Баланс должен быть положительным")


class SAccountCreate(SAccountBalance):
    user_id: int = Field(..., description="ID пользователя")


class SAccount(SAccountCreate):
    id: int = Field(..., description="ID счета")


class SAccountID(BaseModel):
    id: int = Field(..., description="ID счета")
