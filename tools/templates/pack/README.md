# {{title}}

A guide pack for SendaFH, the leveling guide addon for World of Warcraft:
Forever, by {{author}}. It is a separate addon with {{author}}'s own guides;
it is not made by SendaFH.

## For players

1. Install SendaFH first.
2. Download `{{folder}}-<version>.zip` from this project's releases and unzip
   it into the game's `Interface/AddOns/` folder, next to `SendaFH`.
3. Restart the game. The pack's guides appear in SendaFH's guide menu
   (`/sendafh guides`) under Guide packs; Options > Guide packs
   (`/sendafh packs`) turns the pack on or off.

Credits: {{author}}. Licence: {{license}} (see `LICENSE`).

This pack is supported by {{author}}, not by SendaFH: report its problems
here.

## For authors

This pack was started with `sendafh new`, which needs an empty folder: for
your next pack, run `sendafh new` first and `git init` in the folder after
(a folder holding only `.git` counts as not empty).

You need Node 24 or newer, Lua 5.1 and a SendaFH clone with `npm link`
run in it (`sendafh doctor` checks all of it). From this folder:

- `sendafh find <text>`: look up quest, NPC, object, item and guide ids, and
  the inn and flight point names `sethome`, `hearth`, `getfp` and `fly` take.
- `sendafh lint`: check the guides (in VS Code: the default build task).
- `sendafh playtest`: play every guide to the end in the real addon.
- `sendafh dev`: copy the pack into the game's AddOns folder while you work.
- `sendafh pack`: write the release zip to `dist/`.

SendaFH's source describes the guide format on one page in
docs/GUIDE_CHEATSHEET.md, in full in docs/GUIDE_FORMAT.md, and packs in
docs/GUIDE_PACKS.md (what a pack is, what the tools require, what is asked
of authors) and docs/PACKS.md (the full handbook). Start from
`guides/example.guide`.
