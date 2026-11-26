---
name: add-message
description: Add or change a log or Discord text in workshop_changelogs/i18n/translations.py for both English and German. Use whenever code needs a new message.
---

# Add a message

Background: `docs/architecture.md`, section "Invariants".

## Steps

1. Add the key to `EN_MESSAGES` in
   `workshop_changelogs/i18n/translations.py`. Keys are short English
   phrases (e.g. `"Mod updated"`); placeholders are positional `{}`.
2. Add the same key at the same position to `DE_MESSAGES` with the German
   text and the same number of `{}` placeholders. The module warns at import
   when key lists differ; a missing key raises `KeyError` in `translate()`.
3. Use it as `t("<key>", arg1, arg2)` (`from
   workshop_changelogs.i18n.translations import translate as t`).
4. Check: `python -m compileall workshop_changelogs` and `ruff check .`
   (the file has `# ruff: noqa: E501`, long lines are allowed there).
5. Then the `document-change` skill.

## Rules

- No raw user-visible strings in `logger.info/warning` or the Discord
  payload; use a key.
- A new language needs a `<LANG>_MESSAGES` dict and an entry in `MESSAGES`;
  `LANG` selects it by its first two characters.
