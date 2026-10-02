import markdown
import inspect
from justhtml import JustHTML
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class MarkdownHelper:
    """
    markdown helpers
    """

    @staticmethod
    def to_markdown_html(markdown_text: str, sanatize: bool = False) -> str:
        """
        converts markdown to html

        Args:
            markdown_text (str): (sic)

        Returns:
            str: html snippet
        """
        # "extra", "codehilite", , extensions=["extra", NewTabLinkExtension()]
        clean_text = inspect.cleandoc(markdown_text)
        html = markdown.markdown(
            clean_text, extensions=["extra", "codehilite", NewTabLinkExtension()]
        )
        if sanatize:
            doc = JustHTML(html, fragment=True)
            return doc.to_html()
        else:
            return html


class NewTabLinkProcessor(Treeprocessor):
    def run(self, root):
        # Find all <a> tags in the element tree
        for element in root.iter("a"):
            href = element.get("href", "")
            # Match only external links starting with http:// or https://
            if href.startswith("http://") or href.startswith("https://"):
                element.set("target", "_blank")
                # Optional: Security best practice when using target="_blank"
                element.set("rel", "noopener noreferrer")
        return None


class NewTabLinkExtension(Extension):
    def extendMarkdown(self, md):
        # Register the processor with a low priority so it runs near the end
        md.treeprocessors.register(NewTabLinkProcessor(md), "new_tab_links", 15)


# --- Example Usage ---
# text = """
# Check out [Google](https://google.com) or an [Internal Link](/about-us).
# """

# # Pass your custom extension to the markdown converter
# html = markdown.markdown(text, extensions=[NewTabLinkExtension()])
# print(html)
