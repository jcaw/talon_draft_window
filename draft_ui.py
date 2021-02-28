from typing import Optional

from talon.experimental.textarea import TextArea, Span, DarkThemeLabels


class DraftManager:
    """Use to interface with the draft window."""

    def __init__(self):
        self.area = TextArea()
        self.area.title = "Talon Draft"
        self.area.theme = DarkThemeLabels(text_size=20, label_size=20)
        self.area.value = ""
        self.area.register("label", self._update_labels)

    def show(self, text: Optional[str] = None):
        """Show the window. If provided, set text to `text`."""

        if text is not None:
            self.area.value = text
        self.area.show()

    def hide(self):
        """Hide the window."""

        self.area.hide()

    def get_text(self) -> str:
        """Gets the context of the text area"""
        return self.area.value

    def get_rect(self) -> "talon.types.Rect":
        """Get the Rect for the window"""
        return self.area.rect

    def reposition(
        self,
        xpos: Optional[int] = None,
        ypos: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ):
        """Move/resize window, without having to change all properties."""

        rect = self.area.rect
        if xpos is not None:
            rect.x = xpos

        if ypos is not None:
            rect.y = ypos

        if width is not None:
            rect.width = width

        if height is not None:
            rect.height = height

        self.area.rect = rect

    def select_text(
        self, start_anchor, end_anchor=None, include_trailing_whitespace=False
    ):
        """Select word by its anchor (or range with two anchors)."""
        start_char, end_char, last_space = self.anchor_to_range(start_anchor)
        if end_anchor is not None:
            _, end_char, last_space = self.anchor_to_range(end_anchor)

        if include_trailing_whitespace:
            end_char = last_space

        self.area.sel = Span(start_char, end_char)

    def position_caret(self, anchor, after=False):
        """Move caret before `anchor` (or after with `after`)."""
        start_index, end_index, _ = self.anchor_to_range(anchor)

        self.area.sel = end_index if after else start_index

    def anchor_to_range(self, anchor):
        anchors_data = self._calculate_anchors(self._get_visible_text())
        for loop_anchor, start_index, end_index, last_space_index in anchors_data:
            if anchor == loop_anchor:
                return (start_index, end_index, last_space_index)

        raise RuntimeError(f"Couldn't find anchor {anchor}")

    def change_case(self, anchor, case):
        """Change case of a word.

        :param case str: One of ["Title", "lower", "UPPER"]

        """
        # TODO: Switch this to use complex_insert, etc.
        start_index, end_index, _ = self.anchor_to_range(anchor)
        text = self.area[start_index:end_index]
        if case == "lower":
            updated_text = text.lower()
        elif case == "upper":
            updated_text = text.upper()
        elif case == "title":
            updated_text = text[0].upper() + text[1:]
        else:
            raise AssertionError("Invalid case")

        self.area.replace(Span(start_index, end_index), updated_text)

    @staticmethod
    def _iterate_anchor_labels():
        characters = [chr(i) for i in range(ord("a"), ord("z") + 1)]
        for c in characters:
            yield c

        for c in characters:
            for d in characters:
                yield f"{c}{d}"

    @classmethod
    def _calculate_anchors(cls, text):
        """Iterator yielding anchors from the text.

        Anchors are tuples of:

            (anchor, start_word_index, end_word_index, last_space_index)

        Each anchor corresponds to a single word you may want to reference when
        editing.

        - `index` is a character offset from the start of the string (e.g. the
          first character is at index 0)

        - `anchor` is a char or chars you can use to identify it (e.g. 'a', or
          '1').

        """
        line_idx = 1
        char_idx = 0
        word_start_index = None
        word_end_index = None
        anchor_labels = cls._iterate_anchor_labels()

        state = "newline"

        for curr_index, character in enumerate(text):
            next_state = {" ": "space", "\n": "newline"}.get(character, "word")

            # space -> word, space -> newline, word -> newline should yield
            should_yield = word_start_index is not None and (
                next_state == "newline" or (state == "space" and next_state != "space")
            )
            if should_yield:
                yield (
                    next(anchor_labels),
                    word_start_index,
                    word_end_index or curr_index,
                    curr_index,
                )
                word_start_index = None
                word_end_index = None
                last_space_index = None

            if state != "word" and next_state == "word":
                word_start_index = curr_index

            if state == "word" and next_state != "word":
                word_end_index = curr_index

            if next_state == "newline":
                line_idx += 1
                char_idx = 0
            else:
                char_idx += 1
            state = next_state

        if word_start_index is not None:
            yield (next(anchor_labels), word_start_index, len(text), len(text))

    def _update_labels(self, _visible_text):
        """Update label overlay positions."""
        anchors_data = self._calculate_anchors(self._get_visible_text())
        return [
            (Span(start_index, end_index), anchor)
            for anchor, start_index, end_index, _ in anchors_data
        ]

    def _get_visible_text(self):
        # Placeholder for a future method of getting this
        return self.area.value


if False:
    # Some code for testing, change above False to True and edit as desired
    draft_manager = DraftManager()
    draft_manager.show(
        "This is some text\nand another line of text and some more text so that the line gets so long that it wraps a bit.\nAnd a final sentence"
    )
    draft_manager.reposition(xpos=100, ypos=100)
    draft_manager.select_text("c")
