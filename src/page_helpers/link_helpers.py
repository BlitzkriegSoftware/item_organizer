class LinkHelper:
    """
    Renders common links for UI from Data
    """

    @staticmethod
    def format_user(user_id: int, email: str) -> str:
        """
        Format a user for the UI

        Args:
            user_id (int): PK
            email (str): email

        Returns:
            str: hyperlink
        """
        return f"<a target='_blank' href='mailto:{email}' data-kind=user data-id={user_id}>{email}</a>"

    @staticmethod
    def format_attachment(caption: str, link_url: str) -> str:
        """
        Formats an attachment for the ui

        Args:
            caption (str): (sic)
            link_url (str): (sic)

        Returns:
            str: Hyperlink
        """
        return f"<a target='_blank' data-kind=attachment data-id=-1 href='{link_url}'>{caption}</a>"

    @staticmethod
    def format_item_link(relation_caption: str, to_item_id: int, to_title: str) -> str:
        """
        Formats link to another item

        Args:
            caption (str): (sic)
            to_item_id (int): (sic)
            to_title (str): (sic)

        Returns:
            str: Hyperlink
        """
        return f"<a taget='_blank' data-kind=item data-id={to_item_id} href='#{to_item_id}>{relation_caption}: '{to_title}'</a>"
