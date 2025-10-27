from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.theme import Theme
    _RICH_AVAILABLE = True
except Exception:
    _RICH_AVAILABLE = False


def _get_console() -> Optional[Console]:
    if not _RICH_AVAILABLE:
        return None
    theme = Theme(
        {
            "markdown.h1": "bold orange1",
            "markdown.h2": "bold orange1",
            "markdown.h3": "bold orange1",
            "markdown.h4": "bold orange1",
            "markdown.h5": "orange1",
            "markdown.h6": "orange1",
            "markdown.code_block": "dim",
            "markdown.link": "bold cyan",
            "markdown.list_item_prefix": "orange1",
            "table.border": "orange1",
        }
    )
    return Console(theme=theme)


def render_markdown(md_text: str, title: str = "🦊 Kurama Research Report"):
    """Render Markdown to the terminal with a Kurama-orange panel.

    Falls back to plain print if Rich is not available.
    """
    console = _get_console()
    if console is None:
        print("\n" + title + "\n")
        print(md_text)
        return

    md = Markdown(md_text, code_theme="monokai")
    panel = Panel(
        md,
        title=title,
        border_style="orange1",
        expand=True,
        padding=(1, 2),
    )
    console.print(panel)
