# Active when the draft window is open, but not necessarily focussed
tag: user.draft_window_showing
-
hide (draft | dictate): user.draft_hide()

(kill | discard | close) (draft | dictate):
    user.draft_clear()
    user.draft_hide()

# TODO: Extract common stuff into an action
finish:
    content = user.draft_get_text()
    clip.set_text(content)
    user.draft_hide()
    edit.paste()
submit:
    content = user.draft_get_text()
    clip.set_text(content)
    user.draft_hide()
    edit.paste()
    key(enter)
