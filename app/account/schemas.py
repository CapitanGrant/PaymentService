from pydantic import BaseModel, Field


class SAccountBase(BaseModel):
    balance: float = Field(..., gt=0, description="Баланс должен быть положительным")

class SAccountCreate(SAccountBase):
    user_id: int

class SAccount(SAccountCreate):
    id: int