# Active when the draft window is open, but not necessarily focussed
tag: user.draft_window_showing
-
hide (draft | dictate): user.draft_hide()

(kill | discard) (draft | dictate):
    user.draft_clear()
    user.draft_hide()

(submit | transfer) [draft | dictate]:
    content = user.draft_get_text()
    user.draft_hide()
    # TODO: Transfer via paste?
    insert(content)
