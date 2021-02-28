# These are available globally (in command mode)
mode: command
-
(draft | dictate):
    # Toggle for focus
    user.draft_hide()
    user.draft_show()

(draft | dictate) <user.draft_window_position>:
    # Toggle for focus
    user.draft_hide()
    user.draft_show()
    user.draft_named_move(draft_window_position)

(draft | dictate) small:
    # Toggle for focus
    user.draft_hide()
    user.draft_show()
    user.draft_resize(600, 200)

(draft | dictate) large:
    # Toggle for focus
    user.draft_hide()
    user.draft_show()
    user.draft_resize(800, 500)

empty (draft | dictate): user.draft_show("")

(draft | dictate) (that | thing):
    text = edit.selected_text()
    key(backspace)
    user.draft_show(text)

(draft | dictate) all:
    edit.select_all()
    text = edit.selected_text()
    key(backspace)
    user.draft_show(text)
