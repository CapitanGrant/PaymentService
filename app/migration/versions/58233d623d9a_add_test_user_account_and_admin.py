"""Add test user, account, and admin

Revision ID: 58233d623d9a
Revises: 507f2d68e5e0
Create Date: 2025-02-04 11:59:32.208303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column, Integer, String, Boolean, Float
from sqlalchemy.sql import text
from app.users.auth import get_password_hash  # Для хеширования пароля

# revision identifiers, used by Alembic.
revision: str = '58233d623d9a'
down_revision: Union[str, None] = '507f2d68e5e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TEST_USER_ID = 56
TEST_ADMIN_ID = 66

TEST_USERS = [
    {
        "id": TEST_USER_ID,
        "phone_number": "+79919999999",
        "first_name": "Test",
        "last_name": "User",
        "email": "user123@example.com",
        "password": get_password_hash("userpassword"),
        "is_user": True,
        "is_admin": False,
        "is_super_admin": False,
    },
    {
        "id": TEST_ADMIN_ID,
        "phone_number": "+79919999993",
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@example.com",
        "password": get_password_hash("adminpassword"),
        "is_user": False,
        "is_admin": True,
        "is_super_admin": False,
    },
]


def upgrade():
    conn = op.get_bind()

    for user in TEST_USERS:
        conn.execute(
            text(
                "INSERT INTO users (id, phone_number, first_name, last_name, email, password, is_user, is_admin, is_super_admin) "
                "VALUES (:id, :phone_number, :first_name, :last_name, :email, :password, :is_user, :is_admin, :is_super_admin)"
            ),
            user,
        )

    conn.execute(
        text(
            "INSERT INTO accounts (user_id, balance) VALUES (:user_id, :balance)"
        ),
        {"user_id": TEST_USER_ID, "balance": 1000.0},  # Стартовый баланс 1000
    )

    conn.commit()


def downgrade():
    conn = op.get_bind()

    op.execute(text("DELETE FROM users WHERE id IN (:user_id, :admin_id)"),
               {"user_id": TEST_USER_ID, "admin_id": TEST_ADMIN_ID})

    conn.execute(text("DELETE FROM accounts WHERE user_id = :user_id"), {"user_id": TEST_USER_ID})

    conn.commit()
