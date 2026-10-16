'use strict';
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const {spawnSync} = require('node:child_process');
const {runAddon} = require('./helpers/lua');
const ROOT = path.resolve(__dirname, '..');
const MODULES = ['SendaFH','SendaFH_Guides','SendaFH_ItemDB','SendaFH_QuestDB','SendaFH_Codex'];

test('all five addon directories and their TOCs use SendaFH; no old asset paths', () => {
 for(const name of MODULES) assert.ok(fs.existsSync(path.join(ROOT,'addon',name))); 
 for (const name of MODULES) {
  const toc=fs.readFileSync(path.join(ROOT,'addon',name,`${name}.toc`),'utf8');
  if (name !== 'SendaFH') assert.match(toc,/^## Dependencies: SendaFH$/m);
 }
 function walk(dir) {
  for (const p of fs.readdirSync(dir,{withFileTypes:true})) {
   assert.doesNotMatch(p.name,/polestar/i);
   const file=path.join(dir,p.name);
   if(p.isDirectory()) walk(file);
   else if(/\.(lua|xml|toc)$/.test(p.name)) assert.doesNotMatch(fs.readFileSync(file,'utf8'),/Interface[\\/]+AddOns[\\/]+Polestar/);
  }
 }
 walk(path.join(ROOT,'addon'));
});

for (const locale of ['esES','esMX','enUS']) test(`report and invite open Forever Hispano Discord (${locale})`, () => {
 const [r]=runAddon({stubs:['stub_ui.lua'],before:`GetLocale=function() return "${locale}" end`,
  addons:[{name:'SendaFH',files:['Core/Core.xml','Theme/Theme.xml','UI/UI.xml']}],script:`
   uistub.install(); stub.login()
   SendaFH.UI.ShowReport()
   local F=SendaFHReport
   local title, note=F.DiscordTitle:GetText(), F.DiscordNote:GetText()
   F.Invite:Click()
   local invite=SendaFHCopy.Box:GetText()
   SendaFHCopy:Hide()
   SlashCmdList.SENDAFH("discord")
   emit({title=title,note=note,invite=invite,command=SendaFHCopy.Box:GetText(),errors=#SendaFH.Errors()})
  `}).emitted;
 assert.equal(r.invite,'https://discord.gg/qkW5Y8yzk6');
 assert.equal(r.command,r.invite);
 assert.match(r.title,/SendaFH|Forever Hispano/);
 assert.doesNotMatch(r.note,/original|Polestar/);
 if(locale!=='enUS') assert.match(r.note,/Forever Hispano/);
 assert.equal(r.errors,0);
});

test('legacy guide API alias uses the new addon and saved progress', () => {
 const [r]=runAddon({addons:[{name:'SendaFH',files:['Core/Core.xml']}],
 saved:{SendaFH:'SendaFHDB={schema=1,settings={ui={scheme="night"}},sentinel="cuenta"}; SendaFHCharDB={schema=1,manual={test=true},skipped={other=true},flags={ok=true},welcomeSeen=99}'},
 script:'emit({alias=Polestar==SendaFH,name=SendaFH.name,scheme=SendaFH.Get("ui.scheme"),account=SendaFH.DB().sentinel,char=SendaFH.CharState(),new=SendaFH.IsNewCharacter()})'}).emitted;
 assert.equal(r.alias,true); assert.equal(r.name,'SendaFH');assert.equal(r.scheme,'night');
 assert.equal(r.account,'cuenta');assert.equal(r.char.manual.test,true);assert.equal(r.char.skipped.other,true);
 assert.equal(r.char.flags.ok,true);assert.equal(r.new,false);
});

const script=path.join(ROOT,'addon/SendaFH/Migrar-SendaFH.ps1');
function fixture(fn) {
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'sendafh-migration-test-'));
 const account=path.join(dir,'WTF/Account/TEST/SavedVariables');
 const char=path.join(dir,'WTF/Account/TEST/Realm/Hero/SavedVariables');
 fs.mkdirSync(account,{recursive:true});fs.mkdirSync(char,{recursive:true});
 try { fn({dir,account,char}); }
 finally {
  assert.ok(path.resolve(dir).startsWith(path.resolve(os.tmpdir())+path.sep));
  assert.match(path.basename(dir),/^sendafh-migration-test-/);
  fs.rmSync(dir,{recursive:true,force:true});
 }
}
function migrate(dir,args=[]) {
 const r=spawnSync('powershell.exe',['-NoLogo','-NoProfile','-ExecutionPolicy','Bypass','-File',script,'-GamePath',dir,...args],{encoding:'utf8',windowsHide:true});
 assert.equal(r.status,0,r.stdout+'\n'+r.stderr);
 return r;
}
test('migration copies account and character progress, keeps originals and bindings backup, and never overwrites new progress', {skip:process.platform!=='win32'}, () => fixture(({dir,account,char}) => {
 const oldAccount='PolestarDB = { settings = { scheme = "night" }, note = "PolestarDB stays inside player text" }\r\n';
 const oldChar='PolestarCharDB = { manual = { done = true }, tabs = { "guide/one" } }\r\n';
 const oldBindings='bind F6 POLESTAR_NEXT\r\nbind F7 "CLICK PolestarQuestItemButton:LeftButton"\r\nbind F8 JUMP\r\n';
 fs.writeFileSync(path.join(account,'Polestar.lua'),oldAccount);
 fs.writeFileSync(path.join(account,'Polestar.lua.bak'),oldAccount);
 fs.writeFileSync(path.join(char,'Polestar.lua'),oldChar);
 const bindings=path.join(path.dirname(char),'bindings-cache.wtf');fs.writeFileSync(bindings,oldBindings);
 migrate(dir);
 assert.equal(fs.readFileSync(path.join(account,'SendaFH.lua'),'utf8'),oldAccount.replace(/^PolestarDB/,'SendaFHDB'));
 assert.equal(fs.readFileSync(path.join(account,'SendaFH.lua.bak'),'utf8'),oldAccount.replace(/^PolestarDB/,'SendaFHDB'));
 assert.equal(fs.readFileSync(path.join(char,'SendaFH.lua'),'utf8'),oldChar.replace(/^PolestarCharDB/,'SendaFHCharDB'));
 assert.equal(fs.readFileSync(path.join(account,'Polestar.lua'),'utf8'),oldAccount);
 assert.equal(fs.readFileSync(path.join(char,'Polestar.lua'),'utf8'),oldChar);
 assert.equal(fs.readFileSync(bindings,'utf8'),oldBindings.replace('POLESTAR_','SENDAFH_').replace('CLICK Polestar','CLICK SendaFH'));
 const backups=fs.readdirSync(dir).filter(n=>n.startsWith('SendaFH-backup-'));assert.equal(backups.length,1);
 assert.equal(fs.readFileSync(path.join(dir,backups[0],'TEST/Realm/Hero/bindings-cache.wtf'),'utf8'),oldBindings);
 const newProgress='SendaFHCharDB = { manual = { later = true } }';
 fs.writeFileSync(path.join(char,'SendaFH.lua'),newProgress);
 migrate(dir);
 assert.equal(fs.readFileSync(path.join(char,'SendaFH.lua'),'utf8'),newProgress);
 assert.equal(fs.readdirSync(dir).filter(n=>n.startsWith('SendaFH-backup-')).length,1);
}));

test('migration WhatIf plans the copy without writing files', {skip:process.platform!=='win32'}, () => fixture(({dir,account}) => {
 fs.writeFileSync(path.join(account,'Polestar.lua'),'PolestarDB = {}');
 migrate(dir,['-WhatIf']);
 assert.equal(fs.existsSync(path.join(account,'SendaFH.lua')),false);
 assert.equal(fs.readdirSync(dir).some(n=>n.startsWith('SendaFH-backup-')),false);
}));

test('all updated guides keep their gameplay data across esES/esMX and have no missing presentation strings',()=>{
 const script=`
 local omit={title=true,note=true,text=true,pitch=true,description=true,reason=true,label=true,folder=true,_sendaLocale=true}
 local function gameplay(t)
  local out={}
  for k,v in pairs(t) do if not omit[k] then out[k]=type(v)=="table" and gameplay(v) or v end end
  return out
 end
 local all={};local count=0
 for _,h in ipairs(SendaFH.Guides.List()) do count=count+1;local g=SendaFH.Guides.Get(h.id);all[g.id]=gameplay(g) end
 local stats=SendaFH.SendaGuideLocaleStats;local missing=0
 if stats then for _ in pairs(stats.missing) do missing=missing+1 end end
 emit({data=all,count=count,missing=missing,errors=#SendaFH.Errors()})
 `;
 const run=locale=>runAddon({before:`GetLocale=function() return "${locale}" end`,addons:[{name:'SendaFH',files:['Core/Core.xml']},'SendaFH_Guides'],script}).emitted[0];
 const en=run('enUS'); assert.equal(en.count,220);assert.equal(en.errors,0);
 for(const locale of ['esES','esMX']) {const es=run(locale);assert.equal(es.missing,0);assert.equal(es.errors,0);assert.deepEqual(es.data,en.data);}
});
