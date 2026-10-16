'use strict';
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const names=JSON.parse(fs.readFileSync(path.join(root,'locales/esES-names.json'),'utf8'));
const lines=['-- SendaFH / Forever Hispano. Spanish names derived from pfQuest (MIT).',
 '-- Copyright (c) 2017-2021 Eric Mauser (Shagu). See Licenses/pfQuest-MIT.txt.',
 '-- Source and revision: locales/esES-name-sources.json.',
 'local _, ns = ...','local locale = GetLocale and GetLocale() or "esES"',
 'if locale ~= "esES" and locale ~= "esMX" then return end','ns.SendaNames = {'];
for(const [en,es] of Object.entries(names))lines.push(` [${JSON.stringify(en)}] = ${JSON.stringify(es)},`);
lines.push('}');
fs.writeFileSync(path.join(root,'addon/SendaFH/Core/SendaNamesES.lua'),lines.join('\n')+'\n');
console.log('Spanish name aliases:',Object.keys(names).length);
