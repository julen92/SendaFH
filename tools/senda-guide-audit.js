'use strict';
const fs=require('node:fs');
const {runAddon}=require('../tests/helpers/lua');
const [r]=runAddon({before:'GetLocale = function() return "esES" end',addons:['SendaFH','SendaFH_Guides'],script:`
 local s=SendaFH.SendaGuideLocaleStats
 local missing={}
 for text in pairs(s.missing) do missing[#missing+1]=text end
 table.sort(missing)
 emit({guides=s.guides,fields=s.fields,missing=missing,errors=#SendaFH.Errors()})
`}).emitted;
// Empty Lua arrays are serialized as {}, normalize for the report.
if(!Array.isArray(r.missing))r.missing=[];
console.log(JSON.stringify(r,null,2));
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(r,null,2)+'\n');
if(r.guides!==220||r.missing.length||r.errors)process.exitCode=1;
