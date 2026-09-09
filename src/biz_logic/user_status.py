from enum import Enum


class UserStatus(str, Enum):
    """_summary_

    Args:
        str (_type_): (sic)
        Enum (_type_): (sic)

    Returns:
        _type_: valid states
    """
    NOTUSER = "not-user"
    ACTIVE = "active"
    CONFIRM = "confirm"
    DISABLED = "disabled"

    # def make_in_clause(self, field_name: str):
    #     """
    #     Creates an IN clause for a SQL query based on the user statuses.

    #     Args:
    #         field_name (str): The name of the field to create the IN clause for.

    #     Returns:
    #         str: The IN clause for the SQL query.
    #     """
    #     in_clause = ", ".join(f"'{status.value}'" for status in UserStatus)
    #     sql = f"{field_name} IN ({in_clause})"
    #     return sql
