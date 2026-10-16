# Releasing

Releases are built on a maintainer's machine, not in CI: the data addons are
generated from the game client's tables and local sources that are not in the
repository. CI (`.github/workflows/ci.yml`) runs the test suite on every push
and pull request against a fresh clone, where the tests that need built data
skip with a reason.

## What ships

`node tools/sendafh.js pack` writes three files to `dist/`:

| File | Contents |
|---|---|
| `SendaFH-<version>.zip` | `SendaFH` (with `LICENSE` and a player `README.txt`), `SendaFH_Guides`, always `SendaFH_Nav` (Shortest Path Forever's walking router and maps by Cillian Berragan, with its own GPL-3.0-or-later `LICENSE`, `CREDITS.md` and `UPSTREAM.json`; `nav check` must pass), `SendaFH_QuestDB` / `SendaFH_ItemDB` when built, and always `SendaFH_Codex` (with its `LICENSE-DATA.txt`) |
| `SendaFH_Recorder-<version>.zip` | `SendaFH_Recorder` (optional, with `LICENSE`) |
| `SHA256SUMS` | checksums of both zips, in the format `sha256sum -c` reads |

Addon folders sit at the top level of each zip, so a player (or an addon
manager) extracts straight into `Interface/AddOns/`. The zips are
reproducible: the same sources give byte-identical archives.

Guide packs are packed by their authors with `sendafh pack` in the pack
folder (`<pack>/dist/<folder>-<version>.zip`, version from its `pack.json`);
see docs/PACKS.md.

## Version

The version lives in `package.json`, in `guides/pack.json` (the manifest of
our guides' pack: `compile` writes its version into `SendaFH_Guides.toc`)
and in the `## Version` line of every addon TOC. One command sets them all:

```sh
node tools/sendafh.js version            # print it; exit 1 if guides/pack.json or a TOC disagrees
node tools/sendafh.js version 0.2.0      # set package.json, guides/pack.json and every addon TOC
```

Data addons rebuilt later take the version from `package.json`. Versions
follow `x.y.z`; `0.x` releases are betas.

## What a release holds

Releases are built from the full local data build of the steps below.
[THIRD_PARTY.md](../THIRD_PARTY.md) ("Distributing SendaFH") lists what
that puts in the zip: QuestieDB facts in the guide pack, `SendaFH_QuestDB`
and `SendaFH_Codex`, nothing from AtlasLoot, RareScanner or DungeonJournal,
and never the zone crossings pack (`pack` leaves it out). The Codex is part of
SendaFH (Lookup, Dungeons and Rares read it): `pack` stops when
`SendaFH_Codex` is not built, or was built with `--local-extras`, or names
one of those three among its sources.

## Steps

Replace `0.2.0` with the new version throughout.

1. Start from a clean, up-to-date `next` with the game client installed
   (the data build reads its tables and installed addons). Work and pull
   requests for the coming release collect on `next` (the default branch,
   pushed as it goes); `main` holds the latest release and moves only in
   step 7. Releases come in batches, when the maintainer decides.

2. Set the version and rebuild the data, the data addons and the guides:

   ```sh
   node tools/sendafh.js version 0.2.0
   node tools/sendafh.js data build
   node tools/sendafh.js questdb build
   node tools/sendafh.js itemdb build && node tools/sendafh.js gear build
   node tools/sendafh.js codex build        # release-safe; never --local-extras here
   node tools/sendafh.js lint
   node tools/sendafh.js compile
   ```

3. Run the whole suite with the data built (nothing skips for missing data
   now):

   ```sh
   node --test "tests/**/*.test.js"
   ```

4. Pack and check the archives:

   ```sh
   rm -rf dist && node tools/sendafh.js pack
   (cd dist && sha256sum -c SHA256SUMS)
   unzip -l dist/SendaFH-0.2.0.zip      # SendaFH_Codex/ with its LICENSE-DATA.txt, and SendaFH_Nav/ with its LICENSE and CREDITS.md, are listed
   node tools/sendafh.js nav check      # SendaFH_Nav matches its UPSTREAM.json
   ```

5. Smoke-test the zips as a player gets them: unpack both into an empty
   AddOns folder and load the addons from there under Lua 5.1, with the stub
   client the tests use (`SENDAFH_ADDON_DIR` points the test loader at
   another addon folder):

   ```sh
   smoke=$(mktemp -d)
   unzip -q dist/SendaFH-0.2.0.zip -d "$smoke/AddOns"
   unzip -q dist/SendaFH_Recorder-0.2.0.zip -d "$smoke/AddOns"
   SENDAFH_ADDON_DIR="$smoke/AddOns" node --test tests/release.test.js
   rm -rf "$smoke"
   ```

   The test loads every addon in the folder in client order, logs in, and
   checks that the guides registered, a guide opened, the data addons loaded
   and every TOC carries the release version.

6. Then install the zip into the game itself (remove the old `SendaFH*`
   folders first), restart it fully and test what the release changes: play
   the first steps of a guide, and search, Dungeons and Rares when the Codex
   changed. This is a gate: nothing is tagged, pushed or uploaded (steps 7 to
   10) until the maintainer has played the release on their own client and
   said it is good. If the servers are down, the release waits.

7. Commit the version bump and the regenerated files that are tracked
   (`git status` lists them; `SendaFH_QuestDB` and the other local packs are
   ignored) on `next`, bring `main` up to it, tag and push both:

   ```sh
   git add package.json guides/pack.json addon/SendaFH addon/SendaFH_Guides addon/SendaFH_ItemDB addon/SendaFH_Nav addon/SendaFH_Recorder
   git commit -m "Release: 0.2.0"
   git switch main && git merge --ff-only next && git switch next
   git tag -a v0.2.0 -m "SendaFH 0.2.0" main
   git push origin main next v0.2.0
   ```

8. Write the release notes to `dist/notes-0.2.0.md` (`dist/` is not
   committed): what changed for players first (guides, routes, features,
   fixes), then for guide authors and the toolchain. Hours to 60 are the
   simulator's model estimates and are written as such, with the world they
   come from.
   The notes start from CHANGELOG.md's "unreleased" section, which then
   takes the version and the release date. Join each paragraph and list
   item onto one line in the notes: GitHub shows every line break of a
   release's notes, so the changelog's wrapped lines would break mid-sentence.

9. Publish the release with the three files from step 4:

   ```sh
   gh release create v0.2.0 --verify-tag --title "SendaFH 0.2.0" \
     --notes-file dist/notes-0.2.0.md --latest \
     dist/SendaFH-0.2.0.zip dist/SendaFH_Recorder-0.2.0.zip dist/SHA256SUMS
   ```

   A release is a full release, marked Latest, from 0.2.1 on, so the
   repository's Releases box and `releases/latest` point at it; the 0.x
   version and the notes say it is a beta.

10. Upload `dist/SendaFH-0.2.0.zip` to CurseForge (Forever 1.60.1, release
    type Release: CurseForge's app lists a project only once it has one) and
    refresh the project description: the steps and settings are in
    [docs/curseforge/README.md](curseforge/README.md).
