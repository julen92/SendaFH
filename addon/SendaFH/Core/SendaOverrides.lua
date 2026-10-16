-- SendaFH / Forever Hispano. Overrides for community branding and WoW wording.
local _, ns = ...
local locale=GetLocale and GetLocale() or "enUS"
if locale~="esES" and locale~="esMX" then return end
local overrides={
 ["SendaFH"] = "SendaFH",
 ["SendaFH on Discord"] = "Forever Hispano en Discord",
 ["Copy your report with Ctrl+C (Cmd+C on a Mac), switch to Discord and paste it in the SendaFH server. Not in it yet? Get the invite once and open it in your browser."] = "Copia el informe con Ctrl+C (Cmd+C en Mac) y pégalo en el Discord de Forever Hispano. Pulsa Obtener invitación si necesitas el enlace.",
 ["Get the invite"] = "Obtener invitación",
 ["The invite to the SendaFH Discord"] = "Invitación al Discord de Forever Hispano",
 ["Join us on Discord"] = "Discord de Forever Hispano",
 ["Report problems, ask for help and hear about new guides first."] = "Ayuda, fallos y novedades de SendaFH en el Discord de Forever Hispano.",
 ["Report problems, ask for help and hear about new guides first. The invite is selected for you: copy it with Ctrl+C (Cmd+C on a Mac) and open it in your browser."] = "Ayuda, fallos y novedades en el Discord de Forever Hispano. Copia la invitación con Ctrl+C (Cmd+C en Mac) y ábrela en el navegador.",
 ["Discord and its logo are trademarks of Discord Inc.; the logo marks the link to the SendaFH Discord."] = "Discord y su logo pertenecen a Discord Inc. El enlace lleva al Discord de Forever Hispano.",
 ["Inter typeface by The Inter Project Authors, SIL Open Font License 1.1."] = "Polestar: fitzforge y colaboradores. Adaptación: Forever Hispano. SendaFH 0.5.0-beta.1, basado en Polestar 0.2.5-test.1. GPL-3.0-only. Inter: The Inter Project Authors, SIL Open Font License 1.1.",
 ["XP"] = "XP",
 ["%s XP"] = "%s XP",
 ["NPCs"] = "NPC",
 ["Holy (healer)"] = "Sagrado (healer)",
 ["Restoration (healer)"] = "Restauración (healer)",
 ["Target quest mob"] = "Seleccionar mob de misión",
}
for key,value in pairs(overrides) do ns.L[key]=value end
