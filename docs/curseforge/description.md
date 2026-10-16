# SendaFH

**Spanish localization and community adaptation of [Polestar](https://www.curseforge.com/wow/addons/polestar-guides), maintained by Forever Hispano for World of Warcraft: Forever.** Published with the original maintainer's permission, while preserving Polestar's credits and licences.

## What SendaFH adds

- Spanish guide text and an esES/esMX interface, with localized game names where the client or name databases provide them.
- Wording familiar to Spanish WoW players: NPC, leveo, XP and healer, alongside the game's actual quest, item and spell names.
- The Hispano visual theme, with a dark blue background and copper accents.
- The `/senda` and `/sendafh` commands, plus Spanish community support and bug reports.
- Shared translation fixes contributed back to Polestar: [122 improvements in PR #139](https://github.com/fitzforge/polestar/pull/139).

## Guides and features

The included Polestar base provides 220 guides covering leveling, class quests, professions, mounts and other activities. Follow objectives and progress in the guide window, use the navigation arrow and travel planner, browse dungeon quests and access requirements, and check gear advice and XP tracking.

The addon, guide engine, route data and most features originate in Polestar and its credited dependencies. SendaFH adds the Spanish community adaptation; it is not an official Polestar release.

## Install

1. Close WoW completely.
2. Download the SendaFH ZIP from this project's Files tab.
3. Extract its eight `SendaFH` folders directly into your Forever client's `Interface/AddOns` folder.
4. Start the game, enable the modules and type `/senda`.

Keep `WTF` when updating from an earlier SendaFH version. A `/reload` cannot load newly installed modules. Avoid enabling Polestar and SendaFH together. If you want to migrate existing Polestar progress, ask us on Discord before replacing anything.

The archive also includes editable catalogues and build tools under `SendaFH/Source/`; WoW does not load that folder. It explains how to reconstruct the source project alongside the installed Lua.

## Beta status

This first public build is **SendaFH 0.5.0-beta.1**, based on **Polestar v0.2.5-test.1**. Translation and navigation are still being refined. Some Forever-specific names may remain in English, and a walking route can occasionally need correction. The translation is partly AI-assisted and has not been reviewed sentence by sentence by a native speaker.

The current build passed 38 translation/name/module-loading checks and 42 Spanish text-layout checks, plus locale, guide and navigation-data audits. Full route testing in the real game is still pending.

The gallery UI previews are rendered from the addon's actual Lua interface with sample data outside WoW; they are not screenshots of a live play session.

## Español

**SendaFH es la adaptación de Polestar para Forever Hispano:** guías y objetivos en español, vocabulario de WoW, tema Hispano y soporte de nuestra comunidad.

- Acepta y entrega misiones siguiendo la guía, consulta los mobs y objetos que necesitas y usa la flecha para llegar al siguiente objetivo.
- Incluye 220 guías de la base de Polestar: leveo, clases, profesiones, monturas y más contenido.
- Abre la ventana con `/senda`, elige guía con `/senda guides` y entra en los ajustes con `/senda options`.
- Para reportar un paso que falla, usa `/senda report` y copia el informe en nuestro GitHub o Discord.

Para instalar, cierra WoW y descomprime las ocho carpetas directamente en `Interface/AddOns`. Conserva `WTF` al actualizar SendaFH. Si vienes de Polestar, pide ayuda para migrar tu progreso y evita activar ambos addons a la vez.

Esta versión sigue en beta. Parte de la traducción está asistida por IA y algunos nombres exclusivos de Forever pueden seguir en inglés. Si una frase chirría o una ruta falla, cuéntanoslo para corregirlo.

## Credits and support

- **Original project:** [Polestar, by Fitz and contributors](https://www.curseforge.com/wow/addons/polestar-guides).
- **Adaptation, localization and community support:** Forever Hispano.
- **Navigation engine:** [Shortest Path Forever, by Cillian Berragan / cjber](https://github.com/cjber/shortest-path-forever), as integrated and credited by Polestar.
- Original data, translation and font credits are preserved, including Ding!/Yendi, pfQuest/Shagu, Questie, QuestieDB, Carbonite and Inter's authors.
- **License:** GPL-3.0-only for the project, with the original component and data licences retained.
- **Source project:** [SendaFH on GitHub](https://github.com/julen92/SendaFH). Editable sources also accompany the installed Lua in the ZIP.
- **Bug reports:** [SendaFH Issues](https://github.com/julen92/SendaFH/issues/new/choose).
- **Community:** [Forever Hispano on Discord](https://discord.gg/qkW5Y8yzk6).
