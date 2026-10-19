from __future__ import annotations

from identity.user import User
from infrastructure.sqlite.base_repository import SQLiteRepository
from infrastructure.sqlite.mappers.user_mapper import UserMapper
from repositories.user_repository import UserRepository


class SQLiteUserRepository(SQLiteRepository, UserRepository):
    TABLE = "users"

    def add(self, user: User) -> None:
        self._connection.execute(
            """
            INSERT INTO users (id, username, role, is_active, created_at, data)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            tuple(UserMapper.to_record(user).values()),
        )

    def get_by_username(self, username: str) -> User | None:
        row = self._fetch_one(
            "SELECT * FROM users WHERE username = ? COLLATE NOCASE",
            (username,),
        )
        if row is None:
            return None
        record = self._row_to_dict(row)
        assert record is not None
        return UserMapper.from_record(record)
