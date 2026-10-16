'use strict';
// Rebuild the runtime dictionary from the editable Spanish catalogue.
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..');
const catalogue=JSON.parse(fs.readFileSync(path.join(root,'locales/esES-guides.json'),'utf8'));
const quote=s=>JSON.stringify(s).replace(/\\u([0-9a-f]{4})/g,(_,h)=>String.fromCharCode(parseInt(h,16)));
const lines=['-- SendaFH / Forever Hispano. GPL-3.0-only.',
 '-- Generated from locales/esES-guides.json. Includes proper names kept verbatim.',
 'local _, ns = ...','local locale = GetLocale and GetLocale() or "esES"',
 'if locale ~= "esES" and locale ~= "esMX" then return end','ns.SendaGuideText = {'];
for(const [source,spanish] of Object.entries(catalogue)){
 if(typeof spanish!=='string'||!spanish.trim())throw Error('Empty guide translation: '+source);
 if(/ZXQ\d|ERROR\d/.test(spanish))throw Error('Unresolved translation marker: '+source);
 lines.push(` [${quote(source)}] = ${quote(spanish)},`);
}
lines.push('}');
fs.writeFileSync(path.join(root,'addon/SendaFH/Core/SendaGuideES.lua'),lines.join('\n')+'\n');
console.log('Guide dictionary:',Object.keys(catalogue).length,'entries');
