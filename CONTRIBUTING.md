# Contribuir a SendaFH

SendaFH adapta Polestar para Forever Hispano. Conservamos los créditos y las licencias originales;
los arreglos que también sirven para Polestar se proponen al proyecto original.

## Preparar el proyecto

Clona la rama `sendafh`. Necesitas Node.js 24+, Lua 5.1 y Python 3.
El repositorio incluye los ocho módulos publicados y sus fuentes editables.
Los datos generados de esa versión están incluidos; regenerarlos desde las fuentes originales
del cliente requiere las entradas locales descritas por cada herramienta.

```sh
node --test tests/i18n.test.js tests/engine-l10n.test.js tests/names.test.js tests/sendafh-modules.test.js
node tools/senda-locale-audit.js
node tools/senda-guide-audit.js
node tools/sendafh.js nav check
python tools/sendafh-curseforge.py --output ../dist
```

Para comprobar el texto español, ejecuta `node --test tests/text-fit.test.js` con
la variable de entorno `SENDA_TEST_LOCALE=esES`. La CI incluye esta comprobación.

## Traducir

- Interfaz: `addon/SendaFH/Locales/esES.lua` y `esMX.lua`.
- Guías: `locales/esES-guides.json`; genera el Lua con `node tools/senda-build-guide-locale.js`.
- Nombres: `locales/esES-names.json`; genera los datos con `node tools/senda-build-names.js`.
- Preferimos vocabulario de WoW: curar, mobs, leveo, XP, NPC y healer cuando encaje.
- Respeta los nombres del cliente y documenta los nombres exclusivos de Forever sin traducción confirmada.
- Mantén placeholders, IDs, condiciones, coordenadas y claves de protocolo.
- Revisa la diferencia generada y comprueba que no incorpora cambios ajenos al arreglo.

## Mantener nuevas versiones de Polestar

1. Anota tag y commit exactos de la nueva base. Conserva la beta actual para poder volver atrás.
2. Revisa el diff de upstream y sus notas antes de integrar cambios; no reemplaces la adaptación a ciegas.
3. Integra código y datos, manteniendo créditos, licencias y protocolos de packs externos.
4. Actualiza y revisa los catálogos; regenera lo necesario y pasa las comprobaciones.
5. Documenta los cambios reales y prepara una beta para el [plan de pruebas](docs/sendafh/PRUEBAS-BETA.md).
6. Propón por separado a Polestar los arreglos compartidos. Separa traducciones de marca y soporte propios.

Base de esta beta: Polestar `v0.2.5-test.1`, commit
`5445b96713ad1176da173721edd7aa927b29bf1a`.
Las 122 mejoras de esES del [PR #139](https://github.com/fitzforge/polestar/pull/139) ya están integradas.

## Corregir un bug

Abre o enlaza el Issue, reproduce el caso, cambia lo necesario y ejecuta las comprobaciones que
cubran el fallo. Añade una prueba cuando aporte cobertura útil. Documenta qué versión incorpora
el arreglo y pide al jugador que lo compruebe en el cliente real.
No marques una beta como estable sin revisar los criterios del plan de pruebas.
