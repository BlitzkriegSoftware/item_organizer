import os

import pytest
from varname import nameof

from biz_logic.item_manager import ItemManager
from common_helpers.convert_helpers import ConvertHelpers
from data_lib.datalib import DataLib


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

    title = "test test test"
    body = "body body body"

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
        print(f"item_id: {item_id}")

    item_add = ConvertHelpers.safe_to_int(item_id, -1)
    if item_add < 0:
        pytest.fail("invalid item_id")

    note = "note #1"
    result = ItemManager.item_history_add_by_id(item_id, note, user_id)
    if not result:
        pytest.fail("item_history_add_by_id")

    note = "note #2"
    result = ItemManager.item_history_add_by_email(item_id, note, email)
    if not result:
        pytest.fail("item_history_add_by_email")

    ## Fetch item

    # result = ItemManager.item_remove(item_id)
    # if not result:
    #     pytest.fail("item_remove")
