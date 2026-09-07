"""
ISO 8601 / RFC 3339 datetime parsing test cases.

By: Claude AI as modified by author
"""

import datetime

import pytest

from common_helpers.datetime_helpers import DateTimeHelpers


@pytest.mark.parametrize(
    "iso8601, dt",
    [
        pytest.param(
            "2026-09-07T12:00:00Z",
            datetime.datetime(2026, 9, 7, 12, 0, tzinfo=datetime.timezone.utc),
            id="utc-basic",
        ),
        pytest.param(
            "2026-09-07T16:45:30.123456Z",
            datetime.datetime(
                2026, 9, 7, 16, 45, 30, 123456, tzinfo=datetime.timezone.utc
            ),
            id="utc-microseconds",
        ),
        pytest.param(
            "2026-12-25T09:00:00+09:00",
            datetime.datetime(
                2026,
                12,
                25,
                9,
                0,
                tzinfo=datetime.timezone(datetime.timedelta(hours=9)),
            ),
            id="positive-offset-tokyo",
        ),
        pytest.param(
            "2026-07-04T18:30:00-04:00",
            datetime.datetime(
                2026,
                7,
                4,
                18,
                30,
                tzinfo=datetime.timezone(datetime.timedelta(hours=-4)),
            ),
            id="negative-offset-new-york",
        ),
        pytest.param(
            "2026-05-01T08:15:00",
            datetime.datetime(2026, 5, 1, 8, 15),
            id="naive-no-tz",
        ),
        pytest.param(
            "2026-01-01T00:00:00+05:30",
            datetime.datetime(
                2026,
                1,
                1,
                0,
                0,
                tzinfo=datetime.timezone(datetime.timedelta(hours=5, minutes=30)),
            ),
            id="fractional-positive-offset-india",
        ),
        pytest.param(
            "2026-10-31T00:00:00Z",
            datetime.datetime(2026, 10, 31, 0, 0, tzinfo=datetime.timezone.utc),
            id="midnight-utc-boundary",
        ),
        pytest.param(
            "2026-02-28T14:20:00.005000-03:30",
            datetime.datetime(
                2026,
                2,
                28,
                14,
                20,
                0,
                5000,
                tzinfo=datetime.timezone(datetime.timedelta(hours=-3, minutes=-30)),
            ),
            id="fractional-negative-offset-newfoundland",
        ),
        pytest.param(
            "2026-12-31T23:59:59.999999Z",
            datetime.datetime(
                2026,
                12,
                31,
                23,
                59,
                59,
                999999,
                tzinfo=datetime.timezone.utc,
            ),
            id="max-precision-time-boundary",
        ),
        pytest.param(
            "2026-06-15T00:00:00-07:00",
            datetime.datetime(
                2026,
                6,
                15,
                0,
                0,
                tzinfo=datetime.timezone(datetime.timedelta(hours=-7)),
            ),
            id="negative-offset-california",
        ),
    ],
)
def test_iso8601_parses_to_expected_datetime(iso8601, dt):
    """fromisoformat should parse each string to the equivalent datetime."""
    assert DateTimeHelpers.from_iso8601(iso8601) == dt


@pytest.mark.parametrize(
    "iso8601, dt",
    [
        pytest.param(
            "2026-09-07T12:00:00Z",
            datetime.datetime(2026, 9, 7, 12, 0, tzinfo=datetime.timezone.utc),
            id="utc-basic-roundtrip",
        ),
    ],
)
def test_utc_offset_equivalence_z_vs_explicit(iso8601, dt):
    """
    Z and +00:00 represent the same instant. isoformat() renders +00:00,
    not Z, so compare parsed *values*, not raw strings, when round-tripping.
    """
    parsed = DateTimeHelpers.from_iso8601(iso8601)
    assert parsed == dt
    assert parsed.utcoffset() == datetime.timedelta(0)

def test_round_trip(iso8601,dt):
    parsed = DateTimeHelpers.to_iso8601_with_z(dt)
    assert dt == parsed

def test_stamp():
    parsed = DateTimeHelpers.stamp_now_with_z():
    assert parsed is not None