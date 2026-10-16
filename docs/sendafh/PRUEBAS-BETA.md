# Ronda de pruebas de SendaFH 0.5.0-beta.1

Buscamos entre 5 y 10 jugadores para probar la beta leveando. No hay testers asignados todavía.
Las pruebas automáticas no sustituyen estas comprobaciones en el cliente real de Forever.

## Apuntarse

Comenta en el hilo de testers del [hilo de testers de Discord](https://discord.com/channels/1560465332907417712/1560697229977722990)
tu facción, raza, clase, nivel, idioma del cliente y qué zona puedes probar.
El equipo anotará quién cubre cada ruta en la [incidencia de seguimiento de GitHub](https://github.com/julen92/SendaFH/issues/1).
No hace falta empezar un personaje nuevo si puedes cubrir otra zona.

| Ruta inicial | Personajes sugeridos | Idioma | Estado |
| --- | --- | --- | --- |
| Bosque de Elwynn | Humano, clase a elegir | esES | Sin asignar |
| Dun Morogh | Enano o gnomo, clase a elegir | esES | Sin asignar |
| Teldrassil | Elfo de la noche, clase a elegir | esES | Sin asignar |
| Durotar | Orco o trol, clase a elegir | esES | Sin asignar |
| Mulgore | Tauren, clase a elegir | esES | Sin asignar |
| Claros de Tirisfal | No-muerto, clase a elegir | esES | Sin asignar |
| Repetición de una ruta de Alianza | Clase distinta a la primera prueba | esMX | Sin asignar |
| Repetición de una ruta de Horda | Clase distinta a la primera prueba | esMX | Sin asignar |

Las rutas se comprobarán solo si aparecen disponibles para ese personaje y cliente en la beta.
Buscamos variedad de clases; las misiones exclusivas de cada clase necesitan su propia comprobación.

## Antes de empezar

- Cierra WoW, guarda una copia de tus carpetas actuales y conserva `WTF`.
- Instala las ocho carpetas del ZIP de SendaFH; evita activar Polestar a la vez.
- Anota versión del addon, versión del cliente, idioma y otros addons activos.
- Si vienes de Polestar, consulta primero cómo migrar tu progreso en Discord.
- Descarga: [CurseForge](https://www.curseforge.com/wow/addons/sendafh), cuando aprueben la publicación.
  Antes de la aprobación, pide al equipo el paquete de pruebas que ya tenemos preparado.

## Comprobaciones por sesión

- [ ] El addon carga y `/senda` abre la ventana sin errores Lua.
- [ ] La guía correcta aparece y se puede seleccionar.
- [ ] Aceptar una misión actualiza el objetivo de la guía.
- [ ] Matar mobs y recoger objetos actualiza los contadores.
- [ ] Entregar una misión completa el objetivo correspondiente.
- [ ] La flecha llega al NPC u objetivo correcto y el camino se puede recorrer.
- [ ] NPC, misiones y objetos coinciden con el cliente cuando hay traducción disponible.
- [ ] Los textos caben; anota frases cortadas, en inglés o que suenen raras.
- [ ] Las condiciones de clase, raza y facción muestran los pasos que corresponden.
- [ ] `/reload` conserva guía, paso y ajustes.
- [ ] Cerrar WoW y volver a entrar conserva el progreso.
- [ ] Cambiar de zona o guía no deja la flecha en un objetivo anterior.
- [ ] `/senda options` funciona y mantiene los ajustes al volver a entrar.
- [ ] `/senda report` permite copiar el informe del paso.

Marca solo lo probado y anota hasta qué paso has llegado. Vuelos, barcos, zepelines,
mazmorras y rutas de nivel alto se cubren después; una ruta inicial correcta no valida todo el addon.

## Enviar un bug

Un hilo por problema en Discord o un [Issue](https://github.com/julen92/SendaFH/issues/new/choose).
Si existe en ambos, enlaza los dos para mantener un único caso.

```text
Versión de SendaFH y del cliente:
Idioma (esES/esMX):
Facción, raza, clase y nivel:
Guía, zona y paso:
Qué debería pasar:
Qué ha pasado:
Cómo repetirlo / frecuencia:
Informe de /senda report:
Captura / texto completo del error Lua:
```

Para rutas, apunta desde dónde salías y dónde se atasca la flecha. Para traducciones,
incluye el texto actual y tu alternativa. Un nombre exclusivo de Forever sin equivalente
confirmado se registra como pendiente; no se inventa una traducción.

## Orden de los arreglos

1. Error Lua, bloqueo del addon, pérdida de progreso o imposibilidad de continuar una guía.
2. Objetivos que no cuentan, NPC equivocado o ruta imposible.
3. Traducción, textos cortados y detalles visuales.
4. Sugerencias de funciones nuevas.

El equipo reproduce el caso, prepara el cambio y lo comprueba. El jugador confirma el arreglo
en la versión que lo incluye. El changelog debe decir qué versión lo corrige. Un bug de la base
que también afecte a Polestar se propone al proyecto original.

## Cuándo preparar una Release

- Instalación y actualización comprobadas en un cliente real.
- Progreso conservado tras volver a entrar al juego.
- Rutas iniciales comprobadas en ambas facciones y ambos idiomas, con resultados anotados.
- Sin bugs confirmados pendientes que rompan el addon o bloqueen el leveo.
- Limitaciones conocidas publicadas y otras zonas pendientes claramente indicadas.

Este documento es un plan; no certifica que esas pruebas ya hayan pasado.
