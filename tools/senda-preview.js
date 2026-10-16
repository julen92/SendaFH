// Modified by Forever Hispano for SendaFH, 2026-10-16. GPL-3.0-only.
'use strict';
// Forever Hispano adaptation, 2026-10-16. GPL-3.0-only.
// Render the real addon UI using upstream's synthetic WoW client.
const preview=require('./commands/preview');
const source=preview.SCENES.find(s=>s.file==='options-more.svg');
preview.SCENES.push({file:'senda.svg',title:'SendaFH · Forever Hispano — vista previa de la interfaz, fuera de WoW',panels:[{...source.panels[1],before:'GetLocale = function() return "esES" end',script:'SendaFH.version = "0.2.3"; SendaFH.UI.ShowOptions("about")'}]});
preview.run(['senda','guide']).catch(e=>{console.error(e);process.exitCode=1});
