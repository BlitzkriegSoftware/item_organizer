import pytest

from page_helpers.markdown_helpers import MarkdownHelper


def test_markdown_to_html_1():
    md = """
    # Intro
    Some *intro* text
    ## next topic
    next _topic_
    """
    html = MarkdownHelper.to_markdown_html(md)
    print(html)
    assert html is not None
