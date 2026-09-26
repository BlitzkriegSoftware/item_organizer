import pytest
from common_helpers.format_helpers import FormatHelper
from common_helpers.random_helpers import RandomHelper


@pytest.mark.parametrize(
    "tlen,evy,ct",
    [
        (1, 3, 0),
        (2, 3, 0),
        (3, 3, 0),
        (4, 3, 1),
        (5, 3, 1),
        (6, 3, 1),
        (7, 3, 2),
        (8, 3, 2),
        (9, 3, 2),
    ],
)
def test_delimiter_every(tlen: int, evy: int, ct: int):
    delimiter = "-"
    r_text = RandomHelper.random_string(tlen)
    d_text = FormatHelper.delimiter_every(r_text, evy, delimiter)
    print(d_text)
    assert ct == d_text.count(delimiter)
