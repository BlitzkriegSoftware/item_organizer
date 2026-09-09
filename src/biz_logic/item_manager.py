from functools import cache
import os
from varname import nameof
from app_exceptions.configuration_exception import ConfigurationException
from app_exceptions.db_exception import DatabaseException
from app_exceptions.validation_exception import ValidationException
from biz_logic.user_manager import UserManager
from data_lib.datalib import DataLib


class ItemManager:
    """Item Manager is responsible for managing items in the application."""

    @cache
    @staticmethod
    def priority_list_get() -> dict[int, str]:
        priority_list: dict[int, str] = {}
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:
            raise ConfigurationException("missing", "IOR_SCHEMA")

        query = f"select priority_id, priority_title from {IOR_SCHEMA}.priority order by priority_id;"
        result = DataLib.query_return_dict_in_one(query)
        if not result:
            raise DatabaseException("unable (0)", query)

        for row in result:
            id = row["priority_id"]
            text = row["priority_title"]
            priority_list[id] = text

        return priority_list

    @staticmethod
    def item_add(
        title: str,
        body: str,
        org_id: int,
        created_by: int,
        assigned_to: int,
        item_state_id: int,
        priority_id: int,
        rank: int = 0,
    ) -> int:
        item_id: int = -1
        priority_list = ItemManager.priority_list_get()

        if not title:
            raise ValidationException("required", nameof(title), title)
        if not body:
            raise ValidationException("required", nameof(body), body)
        if org_id < 0:
            raise ValidationException("required", nameof(org_id), str(org_id))
        if created_by < 0:
            raise ValidationException("required", nameof(created_by), str(created_by))
        if assigned_to < 0:
            raise ValidationException("required", nameof(assigned_to), str(assigned_to))
        if item_state_id not in UserManager.VALID_USER_ORG_ROLE_IDS:
            raise ValidationException("required", nameof(assigned_to), str(assigned_to))
        if priority_id not in priority_list.keys():
            raise ValidationException("invalid", nameof(priority_id), str(priority_id))

        query = f"INSERT INTO myio.item (title, body, org_id, item_state_id, created_by, assigned_to, priority_id, rank) VALUES ( '{title}', '{body}', {org_id}, {item_state_id}, {created_by}, {assigned_to}, {priority_id}, {rank}) returning item_id;"

        item_id = DataLib.query_return_single_value_in_one(query)
        if not item_id:
            raise DatabaseException("unable (0)", query)

        return item_id

    @staticmethod
    def item_history_add_by_email(
        item_id: int,
        history_note: str,
        history_by: str = "(system)",
    ):
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:
            raise ConfigurationException("missing", "IOR_SCHEMA")

        if item_id < 0:
            raise ValidationException("bad value", nameof(item_id), item_id)
        if not history_note:
            raise ValidationException("must not be empty", nameof(history_note), "")
        if not history_by:
            raise ValidationException("must not be empty", nameof(history_by), "")

        query = f"select {IOR_SCHEMA}.item_history_add({item_id}, '{history_note}', '{history_by}');"
        result = DataLib.query_execute_in_one(query)
        if not result:
            raise DatabaseException(
                f"Failed to add item history for item_id: {item_id} with note: {history_note} by: {history_by}",
                query,
            )

    @staticmethod
    def item_history_add_by_id(
        item_id: int,
        history_note: str,
        history_by: int = -1,
    ):
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:
            raise ConfigurationException("missing", "IOR_SCHEMA")

        if item_id < 0:
            raise ValidationException("bad value", nameof(item_id), item_id)
        if not history_note:
            raise ValidationException("must not be empty", nameof(history_note), "")
        if history_by < -1:
            raise ValidationException("bad value", nameof(history_by), history_by)

        query = f"select {IOR_SCHEMA}.item_history_add_by_id({item_id}, '{history_note}', {history_by});"
        result = DataLib.query_execute_in_one(query)
        if not result:
            raise DatabaseException(
                f"Failed to add item history for item_id: {item_id} with note: {history_note} by: {history_by}",
                query,
            )
