from functools import cache
import os
from varname import nameof
from app_exceptions.configuration_exception import ConfigurationException
from app_exceptions.db_exception import DatabaseException
from app_exceptions.validation_exception import ValidationException
from app_logger.applogger import AppLogger
from data_lib.datalib import DataLib
from psycopg2.extras import RealDictRow


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

    @cache
    @staticmethod
    def item_state_list_get(
        org_id: int,
    ) -> dict[int, str]:
        item_state_list: dict[int, str] = {}
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:
            raise ConfigurationException("missing", "IOR_SCHEMA")

        query = f"select item_state_id, state_title from {IOR_SCHEMA}.item_state where org_id = {org_id} order by item_state_id;"
        result = DataLib.query_return_dict_in_one(query)
        if not result:
            raise DatabaseException("unable (0)", query)

        for row in result:
            id = row["item_state_id"]
            text = row["state_title"]
            item_state_list[id] = text

        return item_state_list

    @staticmethod
    def item_add(
        title: str,
        body: str,
        org_id: int,
        created_by: int,
        assigned_to: int,
        item_state_id: int,
        priority_id: int,
        rankorder: int = 0,
    ) -> int:
        item_id: int = -1

        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:
            raise ConfigurationException("missing", "IOR_SCHEMA")

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

        priority_list = ItemManager.priority_list_get()
        item_state_list = ItemManager.item_state_list_get(org_id)

        if item_state_id not in item_state_list.keys():
            raise ValidationException(
                "required", nameof(item_state_id), str(item_state_id)
            )
        if priority_id not in priority_list.keys():
            raise ValidationException("invalid", nameof(priority_id), str(priority_id))

        query = f"INSERT INTO {IOR_SCHEMA}.item (title, body, org_id, item_state_id, created_by, assigned_to, priority_id, rankorder) VALUES ( '{title}', '{body}', {org_id}, {item_state_id}, {created_by}, {assigned_to}, {priority_id}, {rankorder}) returning item_id;"

        # AppLogger.log_info(query,{}, logger_name=nameof(ItemManager.item_add))

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

        procedure_name = "item_history_add"
        args = (
            item_id,
            history_note,
            history_by,
        )

        result = DataLib.stored_procedure_execute_all_in_one(
            procedure_name, args, IOR_SCHEMA
        )
        if not result:
            raise DatabaseException(
                f"Failed to add item history for item_id: {item_id} with note: {history_note} by: {history_by}",
                procedure_name,
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

        procedure_name = "item_history_add_by_id"
        args = (
            item_id,
            history_note,
            history_by,
        )

        result = DataLib.stored_procedure_execute_all_in_one(
            procedure_name, args, IOR_SCHEMA,
        )
        if not result:
            raise DatabaseException(
                f"Failed to add item history for item_id: {item_id} with note: {history_note} by: {history_by}",
                procedure_name,
            )

    @staticmethod
    def item_remove(
        item_id: int,
    ):
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:
            raise ConfigurationException("missing", "IOR_SCHEMA")

        procedure_name = "item_remove"
        args = (item_id,)

        results = DataLib.stored_procedure_execute_all_in_one(
            procedure_name, args, IOR_SCHEMA
        )

        if not results:
            raise DatabaseException("unable (0)", f"{procedure_name}({item_id})")

    @staticmethod
    def item_get(
        item_id: int,
    ) -> RealDictRow | None:
        return None
