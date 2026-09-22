from page_helpers.link_helpers import LinkHelper


class UserModel:
    def __init__(
        self,
        user_id: int,
        email: str,
    ) -> None:
        self.user_id = user_id
        self.email = email

    def __str__(self) -> str:
        return LinkHelper.format_user(self.user_id, self.email)
