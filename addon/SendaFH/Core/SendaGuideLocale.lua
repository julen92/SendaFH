-- SendaFH / Forever Hispano, 2026-10-16. GPL-3.0-only.
-- Translate presentation only. Names used by secure target buttons, quest IDs,
-- coordinates, condition tokens and travel destinations retain their identity.
local _, ns = ...
local locale = GetLocale and GetLocale() or "esES"
if locale ~= "esES" and locale ~= "esMX" then return end
local display = { title = true, note = true, text = true, pitch = true,
 description = true, reason = true, label = true, folder = true }
local folders = {
 ["Mounts · PvP"] = "Monturas · PvP", ["Mounts · Level 40"] = "Monturas · Nivel 40",
 ["Mounts · Reputation"] = "Monturas · Reputación", ["Mounts · Class"] = "Monturas · Clase",
 ["Mounts · Level 60"] = "Monturas · Nivel 60", ["Mounts · Drops"] = "Monturas · Drops",
 ["Mounts · Legacy"] = "Monturas · Legado", ["Companion pets · Drops"] = "Mascotas · Drops",
 ["Companion pets · Vendors"] = "Mascotas · Vendedores", ["Companion pets · Quests"] = "Mascotas · Misiones",
 ["Companion pets · Legacy"] = "Mascotas · Legado",
}
ns.SendaGuideLocaleStats = { guides = 0, fields = 0, missing = {} }
function ns.LocalizeGuide(def)
 -- Other authors' packs have their own localization; this catalogue is for the bundled guides.
 if def.pack ~= "guides" or def._sendaLocale then return end
 local dict = ns.SendaGuideText or {}
 local stats = ns.SendaGuideLocaleStats
 local seen = {}
 local function visit(t)
  if seen[t] then return end
  seen[t] = true
  for k, value in pairs(t) do
   if type(value) == "table" then visit(value)
   elseif type(value) == "string" and display[k] then
    -- Quest titles are looked up in the client's quest cache when rendered.
    if not (k == "title" and t.quest) then
     local translated = folders[value] or dict[value]
     if translated then t[k] = translated; stats.fields = stats.fields + 1
     elseif value ~= "" then stats.missing[value] = true end
    end
   end
  end
 end
 visit(def)
 def._sendaLocale = locale
 stats.guides = stats.guides + 1
end
