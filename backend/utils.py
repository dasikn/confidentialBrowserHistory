from bs4 import BeautifulSoup
from markdownify import markdownify as md


def clean_html_to_markdown(raw_html: str) -> str:
    """Removes junk and converts HTML structure to Markdown locally."""
    soup = BeautifulSoup(raw_html, "html.parser")

    # Remove noise by tag
    for element in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "svg", "img", "figure"]):
        element.decompose()

    # Convert cleaned HTML to Markdown
    clean_markdown = md(str(soup), heading_style="ATX", strip=["img", "a"])

    # Collapse excessive whitespace
    lines = [line.strip() for line in clean_markdown.splitlines()]
    clean_markdown = "\n".join(line for line in lines if line)

    return clean_markdown
