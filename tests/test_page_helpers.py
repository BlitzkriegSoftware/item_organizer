from page_helpers.link_helpers import LinkHelper


def test_format_user():
    link = LinkHelper.format_user(0, "spookdejur@hotmail.com")
    assert link is not None


def test_format_email():
    link = LinkHelper.format_email("spookdejur@hotmail.com")
    assert link is not None


def test_format_attachment():
    link = LinkHelper.format_attachment("google", "https://google.com")
    assert link is not None


def test_format_item_link():
    link = LinkHelper.format_item_link("Parent", 10, "this bug")
    assert link is not None
