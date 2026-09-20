from functools import cache
import os
from varname import nameof
from app_exceptions.configuration_exception import ConfigurationException
from app_exceptions.db_exception import DatabaseException
from app_exceptions.validation_exception import ValidationException
from app_logger.applogger import AppLogger
from biz_logic.model_attachment import AttachmentModel
from biz_logic.model_relation import RelationModel
from data_lib.datalib import DataLib
from psycopg2.extras import RealDictRow


class ItemManager:
    """Item Manager is responsible for managing items in the application."""

    #
    # Lookups
    #

    @cache
    @staticmethod
    def priority_list_get() -> dict[int, str]:
        priority_list: dict[int, str] = {}
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("missing", "IOR_SCHEMA")

        query = f"select priority_id, priority_title from {IOR_SCHEMA}.priority order by priority_id;"
        result = DataLib.query_return_dict_in_one(query)
        if not result:  # pragma: no cover
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
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("missing", "IOR_SCHEMA")

        query = f"select item_state_id, state_title from {IOR_SCHEMA}.item_state where org_id = {org_id} order by item_state_id;"
        result = DataLib.query_return_dict_in_one(query)
        if not result:  # pragma: no cover
            raise DatabaseException("unable (0)", query)

        for row in result:
            id = row["item_state_id"]
            text = row["state_title"]
            item_state_list[id] = text

        return item_state_list

    @cache
    @staticmethod
    def item_kind_list_get() -> dict[int, str]:
        item_kind_list: dict[int, str] = {}
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("missing", "IOR_SCHEMA")

        query = f"select item_kind_id, kind_title from {IOR_SCHEMA}.item_kind order by item_kind_id;"
        result = DataLib.query_return_dict_in_one(query)
        if not result:  # pragma: no cover
            raise DatabaseException("unable (0)", query)

        for row in result:
            id = row["item_kind_id"]
            text = row["kind_title"]
            item_kind_list[id] = text

        return item_kind_list

    @cache
    @staticmethod
    def item_relationship_list_get() -> dict[int, str]:
        item_relationship_list: dict[int, str] = {}
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("missing", "IOR_SCHEMA")

        query = f"select relationship_id, relationship_title from {IOR_SCHEMA}.relationship  order by relationship_id;"
        result = DataLib.query_return_dict_in_one(query)
        if not result:  # pragma: no cover
            raise DatabaseException("unable (0)", query)

        for row in result:
            id = row["relationship_id"]
            text = row["relationship_title"]
            item_relationship_list[id] = text

        return item_relationship_list

    #
    # Item and related stuff
    #

    @staticmethod
    def item_add(
        title: str,
        body: str,
        org_id: int,
        item_kind_id: int,
        created_by: int,
        assigned_to: int,
        item_state_id: int,
        priority_id: int,
        rankorder: int = 0,
    ) -> int:
        item_id: int = -1

        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:  # pragma: no cover
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
        item_kind_list = ItemManager.item_kind_list_get()

        if item_state_id not in item_state_list.keys():
            raise ValidationException(
                "required", nameof(item_state_id), str(item_state_id)
            )
        if priority_id not in priority_list.keys():
            raise ValidationException("invalid", nameof(priority_id), str(priority_id))
        if item_kind_id not in item_kind_list.keys():
            raise ValidationException(
                "invalid", nameof(item_kind_id), str(item_kind_id)
            )

        query = f"INSERT INTO {IOR_SCHEMA}.item (title, body, org_id, item_kind_id, item_state_id, created_by, assigned_to, priority_id, rankorder) VALUES ( '{title}', '{body}', {org_id}, {item_kind_id}, {item_state_id}, {created_by}, {assigned_to}, {priority_id}, {rankorder}) returning item_id;"

        # AppLogger.log_info(query,{}, logger_name=nameof(ItemManager.item_add))

        item_id = DataLib.query_return_single_value_in_one(query)
        if not item_id:
            raise DatabaseException("unable (0)", query)

        return item_id

    @staticmethod
    def item_remove(
        item_id: int,
    ) -> bool:
        isOk = True
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("missing", "IOR_SCHEMA")

        procedure_name = "item_remove"
        args = (item_id,)

        results = DataLib.stored_procedure_execute_all_in_one(
            procedure_name, args, IOR_SCHEMA
        )

        if not results:  # pragma: no cover
            isOk = False
            raise DatabaseException("unable (0)", f"{procedure_name}({item_id})")

        return isOk

    @staticmethod
    def item_history_add_by_email(
        item_id: int,
        history_note: str,
        history_by: str = "(system)",
    ) -> bool:
        isOk = True
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:  # pragma: no cover
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
        if not result:  # pragma: no cover
            isOk = False
            raise DatabaseException(
                f"Failed to add item history for item_id: {item_id} with note: {history_note} by: {history_by}",
                procedure_name,
            )

        return isOk

    @staticmethod
    def item_history_add_by_id(
        item_id: int,
        history_note: str,
        history_by: int = -1,
    ) -> bool:
        isOk = True
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:  # pragma: no cover
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
            procedure_name,
            args,
            IOR_SCHEMA,
        )
        if not result:  # pragma: no cover
            isOk = False
            raise DatabaseException(
                f"Failed to add item history for item_id: {item_id} with note: {history_note} by: {history_by}",
                procedure_name,
            )

        return isOk

    @staticmethod
    def item_nv_get(item_id: int) -> dict[str, str]:
        """
        Get NV items.

        Args:
            item_id (int): PK

        Raises:
            ConfigurationException: IOR_SCHEMA

        Returns:
            dict[str, str]: NV Items never None
        """
        d: dict[str, str] = {}
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("missing", "IOR_SCHEMA")
        query = f" SELECT it.nv_key ,it.nv_value FROM {IOR_SCHEMA}.item_nv it WHERE it.item_id = {item_id} ORDER BY it.nv_key ASC ;"
        # query = f"SELECT {IOR_SCHEMA}.item_nv_get({item_id})"
        drows = DataLib.query_return_dict_in_one(query)
        if drows:
            for r in drows:
                AppLogger.log_debug(str(r.keys()))
                m_key = r["nv_key"]
                m_value = r["nv_value"]
                d[m_key] = m_value

        return d

    @staticmethod
    def item_nv_add(
        item_id: int,
        nv_key: str,
        nv_value: str,
    ) -> bool:
        """
        Add, Remove, or Update an Name/Value

        If nv_key exists, does an update
        if nv_value is empty, does a delete
        Otherwise adds

        Args:
            item_id (int): (sic)
            nv_key (str): name
            nv_value (str): value

        Raises:
            ConfigurationException: IOR_SCHEMA
            DatabaseException: Execute

        Returns:
            bool: True if so
        """
        isOk = True

        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("missing", "IOR_SCHEMA")

        if not nv_key:
            raise ValidationException("required", nameof(nv_key))

        procedure_name = "item_nv_set"
        args = (
            item_id,
            nv_key,
            nv_value,
        )

        results = DataLib.stored_procedure_execute_all_in_one(
            procedure_name, args, IOR_SCHEMA
        )

        if not results:  # pragma: no cover
            isOk = False
            raise DatabaseException(
                "unable (0)", f"{procedure_name}({item_id}, {nv_key}, {nv_value})"
            )

        return isOk

    @staticmethod
    def item_nv_remove(
        item_id: int,
        nv_key: str,
    ) -> bool:
        isOk = True

        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("missing", "IOR_SCHEMA")

        if not nv_key:
            raise ValidationException("required", nameof(nv_key))

        procedure_name = "item_nv_del"
        args = (item_id, nv_key)

        results = DataLib.stored_procedure_execute_all_in_one(
            procedure_name, args, IOR_SCHEMA
        )

        if not results:  # pragma: no cover
            isOk = False
            raise DatabaseException(
                "unable (0)", f"{procedure_name}({item_id}, {nv_key})"
            )

        return isOk

    @staticmethod
    def item_attachment_get(item_id: int) -> list[AttachmentModel]:
        d: list[AttachmentModel] = []
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("missing", "IOR_SCHEMA")

        query = f"SELECT {IOR_SCHEMA}.item_attachment_get({item_id})"
        drows = DataLib.query_return_dict_in_one(query)
        if drows:
            for r in drows:
                a = AttachmentModel(
                    r["created_by"],
                    r["email"],
                    r["caption"],
                    r["storage_url"],
                    r["created_date"],
                )
                d.append(a)

        return d

    @staticmethod
    def item_attachment_add(
        item_id: int,
        user_id: int,
        caption: str,
        storage_url: str,
    ) -> bool:
        isOk = True
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("missing", "IOR_SCHEMA")

        if item_id < 0:
            raise ValidationException("bad value", nameof(item_id), item_id)
        if not user_id:
            user_id = 0  # system
        if not caption:
            raise ValidationException("must not be empty", nameof(caption), "")
        if not storage_url:
            raise ValidationException("must not be empty", nameof(storage_url), "")

        procedure_name = "item_attachment_set"
        args = (item_id, user_id, caption, storage_url)

        result = DataLib.stored_procedure_execute_all_in_one(
            procedure_name,
            args,
            IOR_SCHEMA,
        )
        if not result:  # pragma: no cover
            isOk = False
            raise DatabaseException(
                f"Failed to add item history for item_id: {item_id} with: {caption} by: {storage_url}",
                procedure_name,
            )

        return isOk

    @staticmethod
    def item_attachment_remove(
        item_id: int,
        storage_url: str,
    ) -> bool:
        isOk = True
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("missing", "IOR_SCHEMA")

        if item_id < 0:
            raise ValidationException("bad value", nameof(item_id), item_id)
        if not storage_url:
            raise ValidationException("must not be empty", nameof(storage_url), "")

        procedure_name = "item_attachment_del"
        args = (
            item_id,
            storage_url,
        )

        result = DataLib.stored_procedure_execute_all_in_one(
            procedure_name,
            args,
            IOR_SCHEMA,
        )
        if not result:  # pragma: no cover
            isOk = False
            raise DatabaseException(
                f"Failed to add item history for item_id: {item_id} by: {storage_url}",
                procedure_name,
            )

        return isOk

    @staticmethod
    def item_relation_get(item_id: int) -> list[RelationModel]:
        d: list[RelationModel] = []
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("missing", "IOR_SCHEMA")

        query = f"SELECT {IOR_SCHEMA}.item_attachment_get({item_id})"
        drows = DataLib.query_return_dict_in_one(query)
        if drows:
            for r in drows:
                a = RelationModel(r["to_id"], r["to_title"], r["re_id"], r["re_text"])
                d.append(a)

        return d

    @staticmethod
    def item_relation_add(
        from_id: int,
        to_id: int,
        relationship_id: int,
    ) -> bool:
        isOk = True
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("missing", "IOR_SCHEMA")

        relation_list = ItemManager.item_relationship_list_get()

        if from_id < 0:
            raise ValidationException("bad value", nameof(from_id), from_id)
        if to_id < 0:
            raise ValidationException("bad value", nameof(to_id), to_id)
        if relationship_id not in relation_list.keys():
            raise ValidationException(
                "invalid", nameof(relationship_id), str(relationship_id)
            )

        procedure_name = "item_attachment_set"
        args = (
            from_id,
            to_id,
            relationship_id,
        )

        result = DataLib.stored_procedure_execute_all_in_one(
            procedure_name,
            args,
            IOR_SCHEMA,
        )
        if not result:  # pragma: no cover
            isOk = False
            raise DatabaseException(
                f"Failed to add item history for item_id: {from_id} to: {to_id} as: {relationship_id}",
                procedure_name,
            )

        return isOk

    @staticmethod
    def item_relation_remove(from_id: int, to_id: int) -> bool:
        isOk = True
        IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")  # noqa: F821
        if not IOR_SCHEMA:  # pragma: no cover
            raise ConfigurationException("missing", "IOR_SCHEMA")

        if from_id < 0:
            raise ValidationException("bad value", nameof(from_id), from_id)
        if to_id < 0:
            raise ValidationException("bad value", nameof(to_id), to_id)

        procedure_name = "item_relation_del"
        args = (
            from_id,
            to_id,
        )

        result = DataLib.stored_procedure_execute_all_in_one(
            procedure_name,
            args,
            IOR_SCHEMA,
        )
        if not result:  # pragma: no cover
            isOk = False
            raise DatabaseException(
                f"Failed to add item history for item_id: {from_id} to: {to_id} as: {relationship_id}",
                procedure_name,
            )

        return isOk
