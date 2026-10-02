import markdown


class MarkdownHelper:
    """
    markdown helpers
    """

    @staticmethod
    def to_markdown_html(markdown_text: str) -> str:
        """
        converts markdown to html

        Args:
            markdown_text (str): (sic)

        Returns:
            str: html snippet
        """
        html = markdown.markdown(markdown_text, extensions=["extra", "codehilite"])
        return html
