-- SendaFH / Forever Hispano. Localize rendered text without changing gameplay data.
local _, ns = ...
if not ns.SendaNames then return end
local aliases, buckets = ns.SendaNames, {}
for en, es in pairs(aliases) do
 local first = en:match("^([%a%d]+)")
 if first then
  local list = buckets[first]
  if not list then list = {}; buckets[first] = list end
  list[#list+1] = { en, es }
 end
end
for _, list in pairs(buckets) do
 table.sort(list, function(a,b) return #a[1] > #b[1] end)
end
local function plain(text)
 if aliases[text] then return aliases[text] end
 local out, pos, last = {}, 1, 1
 while pos <= #text do
  local a,b = text:find("[%a%d]+",pos)
  if not a then break end
  local list = buckets[text:sub(a,b)]
  local found
  if list then
   for i=1,#list do
    local en = list[i][1]
    local stop = a + #en
    if text:sub(a,stop-1) == en and not text:sub(stop,stop):match("[%a%d_]") then
     out[#out+1] = text:sub(last,a-1)
     out[#out+1] = list[i][2]
     last, pos, found = stop, stop, true
     break
    end
   end
  end
  if not found then pos = b+1 end
 end
 out[#out+1] = text:sub(last)
 return table.concat(out)
end
local cache, size = {}, 0
function ns.SendaTranslateText(text)
 if type(text) ~= "string" or text == "" then return text end
 if cache[text] then return cache[text] end
 local result
 if not text:find("|",1,true) then result = plain(text)
 else
  -- WoW links, colour escapes, textures and atlas payloads keep their exact bytes.
  local out, pos = {}, 1
  while pos <= #text do
   local p = text:find("|",pos,true)
   if not p then out[#out+1] = plain(text:sub(pos)); break end
   out[#out+1] = plain(text:sub(pos,p-1))
   local code, stop = text:sub(p+1,p+1), p+1
   if code == "c" and text:sub(p+2,p+9):match("^%x%x%x%x%x%x%x%x$") then stop=p+9
   elseif code == "H" or code == "T" or code == "A" then
    local ending = code == "H" and "|h" or (code == "T" and "|t" or "|a")
    local q = text:find(ending,p+2,true)
    if q then stop=q+1 end
   end
   out[#out+1] = text:sub(p,stop)
   pos = stop+1
  end
  result = table.concat(out)
 end
 if size >= 2048 then cache={}; size=0 end
 cache[text], size = result, size+1
 return result
end

function ns.SendaLocalizeFontString(fs)
 local original = fs.SetText
 fs.SetText = function(self,text) return original(self,ns.SendaTranslateText(text)) end
 if fs.SetFormattedText then
  local formatted = fs.SetFormattedText
  fs.SetFormattedText = function(self,...)
   formatted(self,...)
   local text = self:GetText()
   local translated = ns.SendaTranslateText(text)
   if translated ~= text then original(self,translated) end
  end
 end
 return fs
end

local reverse
function ns.SendaEnglishQuery(text)
 if not ns.Search or not ns.Search.Fold then return text end
 if not reverse then
  reverse={}
  for en,es in pairs(aliases) do
   local key=ns.Search.Fold(es)
   if not reverse[key] or #en < #reverse[key] then reverse[key]=en end
  end
  reverse[ns.Search.Fold("lobos")]="wolf"
  reverse[ns.Search.Fold("lobos jóvenes")]="Young Wolf"
 end
 return reverse[ns.Search.Fold(text)] or text
end
