local Q = SendaFH and SendaFH.QuestDB
if not (Q and Q.AddData) then return end
local add = Q.AddData

add("objects", {
[2843]={"Battered Chest"},
})
