# These are available globally (in command mode)
mode: command
-
^(draft | dictate): user.draft_current_textbox()

^(draft | dictate) <user.draft_window_position>:
    user.draft_show()
    user.draft_named_move(draft_window_position)

^(draft | dictate) small:
    user.draft_show()
    user.draft_resize(600, 200)

^(draft | dictate) large:
    user.draft_show()
    user.draft_resize(800, 500)

^(empty | new) (draft | dictate): user.draft_show("")

^(draft | dictate) (that | thing):
    text = edit.selected_text()
    # TODO: Replace text on submission, e.g. Emacs
    user.draft_show(text)

# ^(draft | dictate) all: user.draft_current_textbox()

^draft <user.complex_phrase>:
    user.draft_show()
    sleep(1s)
    user.insert_complex(complex_phrase, "sentence")
