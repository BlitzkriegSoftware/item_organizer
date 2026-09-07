from enum import Enum


class UserStatus(str, Enum):
    NOTUSER = "not-user"
    ACTIVE = "active"
    CONFIRM = "confirm"
    DISABLED = "disabled"

    def make_in_clause(self, field_name: str):
        in_clause = ", ".join(f"'{status.value}'" for status in UserStatus)
        sql = f"{field_name} IN ({in_clause})"
        return sql
