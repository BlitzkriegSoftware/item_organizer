from page_helpers.link_helpers import LinkHelper


class RelationModel:
    def __init__(
        self,
        to_item_id: int,
        to_title: str,
        relation_id: int,
        relation_title: str,
    ):
        self.to_item_id = to_item_id
        self.to_title = to_title
        self.relation_id = relation_id
        self.relation_title = relation_title

    def __str__(self) -> str:
        r_link = LinkHelper.format_item_link(
            self.relation_title, self.to_item_id, self.to_title
        )
        e_link = f"<a href='' data-kind='relation-edit' data-id='{self.relation_id}'><i class='bi bi-pencil-square'></i></a>"
        return f"<div class='b-relation'>{r_link} {e_link}</div>"
