-- Modified by Forever Hispano for SendaFH, 2026-10-16. GPL-3.0-only.
-- SendaFH / Forever Hispano, 2026-10-16. GPL-3.0-only.
local _, ns = ...
-- Resolve aliases through the existing dispatcher, preserving arguments and guards.
ns.SendaCommandAliases = {
 ayuda = "help", guias = "guides", ["guías"] = "guides", guia = "guide", ["guía"] = "guide",
 siguiente = "next", anterior = "prev", saltar = "skip", ruta = "path",
 mostrar = "show", ocultar = "hide", estado = "status", buscar = "lookup", raros = "rares",
}
ns.RegisterCommand("ajustes", function() ns.Fire("SHOW_OPTIONS") end, "Abrir los ajustes de SendaFH")
ns.RegisterCommand("creditos", function() ns.Fire("SHOW_OPTIONS", "about") end, "Ver autores y licencias")
ns.RegisterCommand("estilo", function()
 ns.Set("ui.scheme", "hispano")
 ns.Set("ui.accent", false)
 ns.Set("ui.bgColor", false)
 ns.Set("ui.matchAccent", false)
 ns.Set("ui.classAccent", false)
 ns.Set("ui.band", false)
 ns.Set("ui.font", "inter")
 ns.Set("ui.matchFont", false)
 ns.Print("Estilo SendaFH aplicado: azul petróleo, cobre y marfil.")
end, "Aplicar el nuevo diseño de SendaFH sin borrar tu progreso")
