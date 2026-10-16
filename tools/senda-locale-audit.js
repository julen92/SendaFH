
'use strict';
const path=require('node:path');
const {localeState}=require('./lib/i18n/project');
function audit(){
 const state=localeState(path.resolve(__dirname,'../addon/SendaFH'),['esES','esMX']);
 const locales={},errors=[];
 for(const [locale,r] of Object.entries(state.locales)){
  locales[locale]={total:state.keys.size,covered:Object.keys(r.translated).length,missing:r.missing};
  if(r.error)errors.push({locale,error:r.error});
  errors.push(...r.problems.map(p=>({locale,...p})),...Object.keys(r.stale).map(key=>({locale,key,error:'stale key'})));
 }
 return {total:state.keys.size,covered:locales.esES.covered,missingCount:locales.esES.missing.length,locales,errors};
}
if(require.main===module){const r=audit();console.log(JSON.stringify(r,null,2));if(r.errors.length||Object.values(r.locales).some(x=>x.missing.length))process.exitCode=1;}
module.exports={audit};
