from fastapi import FastAPI
from app.payment.router import router as payment_router
from app.account.router import router as account_router
from app.users.router import router as router_users
from app.admin_panel.router import router as admin_panel_router

app = FastAPI()


@app.get('/')
def home_page():
    return {"message": "Добро пожаловать! Данное приложение осуществляет "
                       "простое управление CRUD операциями по работе со счетами пользователей!"}


app.include_router(payment_router)
app.include_router(account_router)
app.include_router(router_users)
app.include_router(admin_panel_router)
