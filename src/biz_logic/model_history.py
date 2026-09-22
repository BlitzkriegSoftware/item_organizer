from datetime import datetime

from common_helpers.datetime_helpers import DateTimeHelpers
from page_helpers.link_helpers import LinkHelper


class HistoryModel:
    def __init__(
        self,
        created_date: datetime,
        email: str,
        note: str,
        row_num: int,
    ):
        self.created_date = created_date
        self.email = email
        self.note = note
        self.row_num = row_num

    def __str__(self) -> str:
        d_link = DateTimeHelpers.to_iso8601_with_z(self.created_date)
        u_link = LinkHelper.format_email(self.email)
        return f"<div class='b-history'>[{self.row_num}] {d_link} {u_link} {self.note}</div>"
