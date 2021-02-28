from typing import Optional

from talon import ui, Module, Context
from .draft_ui import DraftManager

from user.utils.formatting import SurroundingText


mod = Module()
ctx = Context()
mod.tag("draft_window_showing", desc="Tag set when draft window showing")

draft_manager = DraftManager()


@mod.action_class
class Actions:
    def draft_show(text: Optional[str] = None):
        """Show draft window"""
        draft_manager.show(text)
        ctx.tags = ["user.draft_window_showing"]

    def draft_hide():
        """Hide draft window"""
        draft_manager.hide()
        ctx.tags = []

    def draft_clear():
        """Delete all text in draft window."""
        draft_manager.area.value = ""

    def draft_select(
        start_anchor: str, end_anchor: str = "", include_trailing_whitespace: int = 0
    ):
        """Selects text in the draft window"""
        draft_manager.select_text(
            start_anchor,
            end_anchor=None if end_anchor == "" else end_anchor,
            include_trailing_whitespace=include_trailing_whitespace == 1,
        )

    def draft_position_caret(anchor: str, after: int = 0):
        """Positions the caret in the draft window"""
        draft_manager.position_caret(anchor, after=after == 1)

    def draft_change_case(anchor: str, case: str):
        """Positions the caret in the draft window"""
        draft_manager.change_case(anchor, case)

    def draft_get_text() -> str:
        """Returns the text in the draft window"""
        return draft_manager.get_text()

    def draft_resize(width: int, height: int):
        """Resize the draft window."""
        draft_manager.reposition(width=width, height=height)

    def draft_named_move(name: str, screen_number: Optional[int] = None):
        """Move the draft window to a named position on screen.

        Options are top, bottom, left, right, or middle.

        """
        screen = ui.screens()[screen_number or 0]
        window_rect = draft_manager.get_rect()
        xpos = (screen.width - window_rect.width) / 2
        ypos = (screen.height - window_rect.height) / 2

        if name == "top":
            ypos = 50
        elif name == "bottom":
            ypos = screen.height - window_rect.height - 50
        elif name == "left":
            xpos = 50
        elif name == "right":
            xpos = screen.width - window_rect.width - 50
        elif name == "middle":
            # That's the default values
            pass

        draft_manager.reposition(xpos=xpos, ypos=ypos)


# TODO: Expand anchors to take any character?
@mod.capture(rule="{self.letter}+")
def draft_anchor(m) -> str:
    """An anchor (string of letters)"""
    return "".join(m)


@mod.capture(rule="(top | bottom | left | right | middle)")
def draft_window_position(m) -> str:
    """One of the named positions you can move the window to"""
    return "".join(m)


draft_window_context = Context()
draft_window_context.matches = r"""
title: Talon Draft
tag: user.draft_window_showing
"""


@draft_window_context.action_class("user")
class DraftWindowActions:
    def surrounding_text() -> Optional[SurroundingText]:
        area = draft_manager.area
        return SurroundingText(
            text_before=area[area.sel.left - 50 : area.sel.left],
            text_after=area[area.sel.right : area.sel.right + 50],
        )
