# Active when we have focus on the draft window
title: Talon Draft
tag: user.draft_window_showing
-
tag(): user.free_dictation

# Position cursor before word
move <user.draft_anchor>:
  user.draft_position_caret("{draft_anchor}")

[move] before <user.draft_anchor>:
  user.draft_position_caret("{draft_anchor}")

# Position cursor after word
[move] after <user.draft_anchor>:
  user.draft_position_caret("{draft_anchor}", 0, 1)

# Select a whole word
(sell | select) <user.draft_anchor>:
  user.draft_select("{draft_anchor}")

# Select a range of words
(sell | select) <user.draft_anchor> to <user.draft_anchor>:
  user.draft_select("{draft_anchor_1}", "{draft_anchor_2}")

# Delete a word
(kill | delete) <user.draft_anchor>:
  user.draft_select("{draft_anchor}", "", 1, 1)
  key(backspace)

# Delete a range of words
(kill | delete) <user.draft_anchor> to <user.draft_anchor>:
  user.draft_select("{draft_anchor_1}", "{draft_anchor_2}", 1, 1)
  key(backspace)

# Make a word title case
word title <user.draft_anchor>:
    user.draft_change_case("{draft_anchor}", "title")

# Make a word lower case
word lower <user.draft_anchor>:
    user.draft_change_case("{draft_anchor}", "lower")

# Make a word all caps case
word upper <user.draft_anchor>:
    user.draft_change_case("{draft_anchor}", "upper")
