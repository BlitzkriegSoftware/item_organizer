from datetime import datetime
import os
from pydoc import Helper

import pytest
from varname import nameof

from app_logger.applogger import AppLogger
from biz_logic.item_manager import ItemManager
from biz_logic.model_user import UserModel
from common_helpers.convert_helpers import ConvertHelpers
from data_lib.datalib import DataLib
from test_helpers.test_helper import TestHelper
from biz_logic.model_attachment import AttachmentModel


def test_priority_list_get():
    priority_list = ItemManager.priority_list_get()
    print(priority_list)
    assert priority_list is not None


def get_user(IOR_SCHEMA: str) -> UserModel:
    user_result = DataLib.query_return_dict_in_one(
        f"select user_id, email from {IOR_SCHEMA}.user order by user_id DESC limit 1;"
    )
    if not user_result:
        pytest.fail("no test data (0)")
    else:
        user_id = ConvertHelpers.safe_to_int(user_result[0]["user_id"], -1)
        email = user_result[0]["email"]

    return UserModel(user_id, email)


def make_item(
    IOR_SCHEMA: str,
    index: int,
    user: UserModel,
    org_id: int,
    title: str,
    body: str,
) -> int:
    created_by = user.user_id
    assigned_to = user.user_id

    item_state_list = ItemManager.item_state_list_get(org_id)
    item_state_id = next(iter(item_state_list))

    priority_list = ItemManager.priority_list_get()
    priority_id = next(iter(priority_list))

    item_kind_list = ItemManager.item_kind_list_get()
    item_kind_id = next(iter(item_kind_list))

    rankorder = 99

    item_id = ItemManager.item_add(
        title,
        body,
        org_id,
        item_kind_id,
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

    return item_id


def test_item_round_trip():
    IOR_SCHEMA = os.getenv("IOR_SCHEMA", "")
    if not IOR_SCHEMA:
        pytest.fail("IOR_SCHEMA missing")

    user = get_user(IOR_SCHEMA)
    title = TestHelper.random_string(10)
    body = TestHelper.random_string(25)
    org_id = 0

    relations = ItemManager.item_relationship_list_get()

    # Item

    item_id_1 = make_item(IOR_SCHEMA, 0, user, org_id, title, body)

    drows = DataLib.query_return_dict_in_one(
        f"select * from {IOR_SCHEMA}.item where item_id = {item_id_1};"
    )
    if not drows:
        pytest.fail("no item results data (1)")

    # History

    note = f"note #1 {title}"
    result = ItemManager.item_history_add_by_id(item_id_1, note, user.user_id)
    if not result:
        pytest.fail("item_history_add_by_id")

    note = f"note #2 {body}"
    result = ItemManager.item_history_add_by_email(item_id_1, note, user.email)
    if not result:
        pytest.fail("item_history_add_by_email")

    history = ItemManager.item_history_get(item_id_1, 0, 10)
    if not history:
        pytest.fail("No history")

    # Name Values

    nv: dict[str, str] = {"n1": "v1", "n2": "v2", "n3": "v3"}

    for nv_key in nv:
        nv_value = nv[nv_key]
        ItemManager.item_nv_add(item_id_1, nv_key, nv_value)

    d = ItemManager.item_nv_get(item_id_1)
    if not d:
        pytest.fail("no nv rows")
    else:
        AppLogger.log_info("nv success", {}, nameof(test_item_round_trip))

    # Attachments

    attach: dict[str, str] = {
        "file1": "\\\\fs:file1",
        "file2": "\\\\fs:file2",
        "url3": "https://sto1/file3",
        "url4": "https://sto1/file4",
    }

    for fn in attach:
        url = attach[fn]
        result = ItemManager.item_attachment_add(item_id_1, 1, fn, url)
        if not result:
            pytest.fail("No add attachment")

    la: list[AttachmentModel] = ItemManager.item_attachment_get(item_id_1)
    if not la:
        pytest.fail("no attachment rows")

    # Tags

    tags: list[str] = ["blue", "moo", "cows", "are", "fun"]

    for t in tags:
        result = ItemManager.item_tag_add(item_id_1, t)
        if not result:
            pytest.fail("failed to add tag")

    result = ItemManager.item_tag_remove(item_id_1, tags[0])
    if not result:
        pytest.fail("no remove tag")

    tags = ItemManager.item_tag_get(item_id_1)
    if not tags:
        pytest.fail("no tags gotten")

    # Relations
    title = TestHelper.random_string(12)
    body = TestHelper.random_string(35)
    org_id = 0

    item_id_2 = make_item(IOR_SCHEMA, 1, user, org_id, title, body)

    ri = next(iter(relations))

    result = ItemManager.item_relation_add(item_id_1, item_id_2, ri)
    if not result:
        pytest.fail("Unable to add relation")

    r_list = ItemManager.item_relation_get(item_id_1)
    if not r_list:
        pytest.fail("Unable to add relation")

    # clean up

    # result = ItemManager.item_remove(item_id)
    # if not result:
    #     pytest.fail("item_remove 1")
    # result = ItemManager.item_remove(item_id_2)
    # if not result:
    #     pytest.fail("item_remove 2")
