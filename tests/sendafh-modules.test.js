'use strict';
const {test}=require('node:test');
const assert=require('node:assert/strict');
const {runAddon}=require('./helpers/lua');
for(const locale of ['esES','esMX']) test(`new SendaFH release: all eight modules load together (${locale})`,()=>{
 const [r]=runAddon({stubs:['stub_world.lua','stub_ui.lua'],before:`GetLocale=function() return "${locale}" end`,
 addons:['SendaFH','SendaFH_Guides','SendaFH_ItemDB','SendaFH_QuestDB','SendaFH_Codex','SendaFH_Names_esES','SendaFH_Names_esMX','SendaFH_Nav'],
 script:`
 uistub.install();stub.login()
 local g=SendaFH.SendaGuideLocaleStats
 SendaFH.UI.ShowReport()
 SendaFHReport.Invite:Click()
 emit({npc=SendaFH.Names.Npc(196),wolf=SendaFH.SendaTranslateText("Young Wolves"),
  invite=SendaFHCopy.Box:GetText(),guides=g.guides,errors=SendaFH.Errors(),
  base=SendaFH.upstreamVersion,commands=SLASH_SENDAFH3})
 `}).emitted;
 assert.equal(r.npc,'Eagan Desollapelambres');assert.equal(r.wolf,'Lobos jóvenes');
 assert.equal(r.invite,'https://discord.gg/qkW5Y8yzk6');assert.equal(r.guides,220);
 assert.equal(Object.keys(r.errors).length,0);assert.equal(r.base,'0.2.5-test.1');assert.equal(r.commands,'/senda');
});
