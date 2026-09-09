import pytest

from biz_logic.item_manager import ItemManager


def test_priority_list_get():
    list = ItemManager.priority_list_get()
    print(list)
    assert list is not None
