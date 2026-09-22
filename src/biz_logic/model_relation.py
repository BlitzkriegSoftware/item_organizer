from page_helpers.link_helpers import LinkHelper


class RelationModel:
    def __init__(
        self,
        to_item_id: int,
        to_title: str,
        relation_id: int,
        relation_text: str,
    ):
        self.to_item_id = to_item_id
        self.to_title = to_title
        self.relation_id = relation_id
        self.caption = relation_text

    def __str__(self) -> str:
        r_link = LinkHelper.format_item_link(
            self.caption, self.to_item_id, self.to_title
        )
        return f"<div class='b-relation'>{r_link}</div>"
