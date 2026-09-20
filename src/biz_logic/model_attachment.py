import datetime
from common_helpers.datetime_helpers import DateTimeHelpers
from page_helpers.link_helpers import LinkHelper


class AttachmentModel:
    def __init__(
        self,
        created_by: int,
        email: str,
        caption: str,
        storage_url: str,
        file_hash: str,
        created_on: datetime.datetime,
    ):
        self.created_by = created_by
        self.email = email
        self.caption = caption
        self.file_url = storage_url
        self.file_hash = file_hash
        self.created_on = created_on

    def __str__(self) -> str:
        d_link = DateTimeHelpers.to_iso8601_with_z(self.created_on)
        u_link = LinkHelper.format_user(self.created_by, self.email)
        a_link = LinkHelper.format_attachment(self.caption, self.file_url)
        return f"{d_link} {u_link} {a_link}"
