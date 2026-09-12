import os
from pydoc import Helper

import pytest
from varname import nameof

from app_logger.applogger import AppLogger
from biz_logic.item_manager import ItemManager
from common_helpers.convert_helpers import ConvertHelpers
from data_lib.datalib import DataLib
from test_helpers.test_helper import TestHelper


def test_priority_list_get():
    priority_list = ItemManager.priority_list_get()
    print(priority_list)
    assert priority_list is not None


def test_item_round_trip():
    IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
    if not IOR_SCHEMA:
        pytest.fail("IOR_SCHEMA missing")

    user_result = DataLib.query_return_dict_in_one(
        f"select user_id, email from {IOR_SCHEMA}.user order by user_id DESC limit 1;"
    )
    if not user_result:
        pytest.fail("no test data (0)")
    else:
        user_id = ConvertHelpers.safe_to_int(user_result[0]["user_id"], -1)
        email = user_result[0]["email"]

    created_by = user_id
    assigned_to = user_id

    org_id = 0
    item_state_list = ItemManager.item_state_list_get(org_id)
    print(nameof(item_state_list), item_state_list)
    item_state_id = next(iter(item_state_list))

    priority_list = ItemManager.priority_list_get()
    print(nameof(priority_list), priority_list)
    priority_id = next(iter(priority_list))

    title = TestHelper.random_string(10)
    body = TestHelper.random_string(25)

    # AppLogger.log_info(f"test_item_round_trip: title={title}, body={body}, org_id={org_id}, created_by={created_by}, assigned_to={assigned_to}, item_state_id={item_state_id}, priority_id={priority_id}")

    rankorder = 99

    item_id = ItemManager.item_add(
        title,
        body,
        org_id,
        created_by,
        assigned_to,
        item_state_id,
        priority_id,
        rankorder,
    )

    if not item_id:
        pytest.fail("Bad item_add()")
    else:
        AppLogger.log_info(f"item_id: {item_id}")

    item_id = ConvertHelpers.safe_to_int(item_id, -1)
    if item_id < 0:
        pytest.fail("invalid item_id")

    drows = DataLib.query_return_dict_in_one(
        f"select * from {IOR_SCHEMA}.item where item_id = {item_id};"
    )
    if not drows:
        pytest.fail("no item results data (1)")

    note = f"note #1 {title}"
    result = ItemManager.item_history_add_by_id(item_id, note, user_id)
    if not result:
        pytest.fail("item_history_add_by_id")

    note = f"note #2 {body}"
    result = ItemManager.item_history_add_by_email(item_id, note, email)
    if not result:
        pytest.fail("item_history_add_by_email")

    query = f"SELECT {IOR_SCHEMA}.item_history_get({item_id}, 10, 0);"
    drows = DataLib.query_return_dict_in_one(query)
    if not drows:
        pytest.fail("no history results data (3)")

    nv: dict[str, str] = {"n1": "v1", "n2": "v2", "n3": "v3"}

    for nv_key, nv_value in nv:
        ItemManager.item_nv_add(item_id, nv_key, nv_value)

    drows = ItemManager.item_nv_get(item_id)
    if not drows:
        pytest.fail("no nv rows")
    else:
        AppLogger.log_info("nv success", {}, nameof(test_item_round_trip))

    # result = ItemManager.item_remove(item_id)
    # if not result:
    #     pytest.fail("item_remove")
