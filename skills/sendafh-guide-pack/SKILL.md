---
name: sendafh-guide-pack
description: Writes, fixes and builds SendaFH guide packs, addons of .guide files (leveling routes, profession and collectible guides) that the SendaFH addon for World of Warcraft Forever loads. Use when creating a pack with `sendafh new`, writing or editing .guide files, looking up quest, NPC, item or object ids with `sendafh find`, fixing `sendafh lint` or `sendafh playtest` problems, or building a pack's release zip.
compatibility: Needs a SendaFH clone with its reference data built (data/forever), Node 24 or newer, and Lua 5.1 or LuaJIT for playtest.
---

# Writing SendaFH guide packs

A guide pack is a folder with a `pack.json` and `.guide` text files. SendaFH's
tools check the guides against the game's data, play them to the end without
the game, and build the addon. The `sendafh` command comes from a SendaFH
clone (`npm link` in it); without it, run
`node <sendafh clone>/tools/sendafh.js <command>` instead. Run every
command from the pack's folder.

The guide format, every line of it: [references/guide-format.md](references/guide-format.md).
Read it before writing a guide.

## Ground rules

- **An id or a coordinate is a guess until `find`, `lint` and `playtest`
  confirm it.** Look up every quest, NPC, object and item id, every inn and
  flight point name and every guide id with `sendafh find` before you write
  it. Never write one from memory: ids in this game differ from other
  versions of it. When `find` has no match, say so to the author instead of
  inventing a value.
- **Leave out what the data fills in.** `accept 7` is enough: the compiler
  adds the title, the quest giver and the coordinates. Type coordinates only
  for `goto` and `explore`, or for a place the data does not know.
- **Routes a player can do alone.** A leveling guide never requires an elite,
  a dungeon or a group quest: lint stops required elite work. Group content
  goes in as an `optional` goal with the tip `<Name> is elite: grouping up is
  advised.`
- **The author's own material only.** Write from the author's notes, routes
  they played (`sendafh record`) or guides they wrote. Never copy text, step
  lists or routes from guides you did not write, SendaFH's own guides
  included: hand over to them with `next` instead.
- **Pack naming.** `pack.json`'s `title` is the pack's own name
  (`Joe's Routes`), one that cannot be taken for SendaFH's own addons. The
  build titles the addon "SendaFH Pack: Joe's Routes" and groups it under
  SendaFH in the game's AddOns list; the addon page should say the same:
  a guide pack for SendaFH, by its author. Every guide id starts with the
  pack id and a slash (`joe-routes/westfall`).

## Workflow

1. **Start the pack** (skip when `pack.json` exists). The folder must be
   empty or missing:

   ```sh
   sendafh new joe-routes --id joe-routes --title "Joe's Routes" --author Joe --yes
   cd joe-routes
   ```

   It writes `pack.json`, `guides/example.guide` (a guide that lints and
   plays: replace it), README, LICENSE and editor and CI files.
   `sendafh doctor` checks Node, Lua and the reference data when a command
   fails for want of them.

2. **Look up every id and place**, as JSON:

   ```sh
   sendafh find "Kobold Camp Cleanup" --kind quest --json   # the quest, its giver, turn-in and objectives
   sendafh find 7 --kind quest --json                       # a quest by id
   sendafh find "Kobold Vermin" --kind npc --json           # an NPC or mob
   sendafh find --kind inn --faction Alliance               # names sethome and hearth take
   sendafh find --kind flight --faction Alliance            # names getfp and fly take
   sendafh find westfall --kind guide --race Human          # SendaFH guides to hand over to with next
   ```

   A number matches every kind with that id (`find 783` prints quest 783,
   NPC 783 and item 783): add `--kind`. Each result's `line` is a guide line
   ready to paste. A quest's `objectives` list each objective's `index` (the
   `n` of `quest <id>.<n>`, numbered as the quest log lists them) and the
   `id` of the mob, item or object it needs: use that id in the `kill`,
   `collect` or `interact`, not one found by name (a name search for
   "Mottled Boar" also returns Dire and Elder Mottled Boars).

3. **Write the guide** in `guides/<name>.guide` with the ids found. Keep a
   step to one place or one batch of work. A step is done when every goal in
   it that is not `optional` is.

4. **Lint until it reports no errors and no warnings:**

   ```sh
   sendafh lint --format json
   ```

   Each diagnostic has `file`, `line`, `severity`, `message` and often a
   `hint` saying how to fix it. `"ok": true` only means no errors: a wrong
   objective number (`quest 788.2` for a quest with one objective) is a
   warning, and playtest still passes. Fix every warning too, or tell the
   author why one stays (new Forever content the data does not know yet).
   Aim for `"errors": 0, "warnings": 0`; run lint again after every change.

5. **Playtest until every guide plays to the end:**

   ```sh
   sendafh playtest
   sendafh playtest --filter westfall --class Mage   # one guide, one class
   ```

   Every line must read `ok`. A `stuck ... at step N` line names the goal the
   simulated character could not finish: a wrong id, an objective number, a
   goal for a quest it never got, a place it cannot reach. Fix it and run
   lint and playtest again.

6. **Try it and build it.** `sendafh play` opens the real addon in a
   browser with the pack loaded; `sendafh install` copies the pack into the
   game, and `sendafh dev` rebuilds it there on every save. When lint and
   playtest pass:

   ```sh
   sendafh pack      # writes dist/<folder>-<version>.zip
   ```

   Raise `version` in `pack.json` for each release.

## Example

A short guide, every id from `sendafh find`, that lints clean and plays to
the end (write your pack id in place of `joe-routes`):

```
guide joe-routes/northshire
title Northshire Valley
faction Alliance
race Human
levels 1-4
zone Elwynn Forest

step Deputy Willem
  accept 783                    -- He stands at the abbey gate
  turnin 783
  accept 7

step Kobold camp
  tip Pull one kobold at a time.
  kill 6 x10 quest 7.1

step Back to the abbey
  turnin 7
```

`quest 7.1` ties the kills to the quest's first objective, so the guide
window counts them from the quest log. A `kill` without it is a check-off the
player ticks by hand.

## When something is unclear

- `sendafh help <command>` lists every option of a command.
- SendaFH's docs in the clone: `docs/GUIDE_PACKS.md` (what a pack is and
  how to publish one), `docs/GUIDE_FORMAT.md` (the full format and every
  lint check), `docs/GUIDE_CHEATSHEET.md` (every line on one page),
  `docs/PACKS.md` (the pack handbook, with every lint message and its fix)
  and `docs/PACK_FORMAT.md` (pack.json and the built addon).
