# Active when the draft window is open, but not necessarily focussed
tag: user.draft_window_showing
-
hide (draft | transfer): user.draft_hide()

kill (draft | transfer):
    user.draft_clear()
    user.draft_hide()

(submit | transfer) [draft | dictate]:
    content = user.draft_get_text()
    user.draft_hide()
    # TODO: Insert, instead of paste?
    user.paste(content)
