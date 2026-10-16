#!/usr/bin/env python3
"""Package the eight SendaFH modules and their editable build sources."""
from pathlib import Path
import argparse,hashlib,json,re,zipfile

ROOT=Path(__file__).resolve().parents[1]
VERSION='0.5.0-beta.1'
MODULES=('SendaFH','SendaFH_Guides','SendaFH_ItemDB','SendaFH_QuestDB','SendaFH_Codex','SendaFH_Nav','SendaFH_Names_esES','SendaFH_Names_esMX')
SKIP={'.git','node_modules','__pycache__','Source'}
SHELL={'.exe','.dll','.cmd','.bat','.ps1','.msi'}
SOURCE_NOTICE='''SendaFH: editable sources\n\nThe installed Lua is source code. This folder adds the guide sources,\ntranslation catalogues, build tools, documentation and licences used by this\nadaptation. It is not loaded by WoW. Original licences and credits apply.\n\nTo reconstruct the project outside your game folder:\n1. Copy the contents of this Source folder into a new project directory.\n2. Create an addon directory there. Copy the eight installed SendaFH folders\n   into addon, omitting SendaFH/Source from that copy to avoid recursion.\n3. With Node.js 24+, Lua 5.1 and Python 3 installed, run:\n   node tools/senda-locale-audit.js\n   node tools/senda-guide-audit.js\n   python tools/sendafh-curseforge.py --output ../dist\n\nThe original Polestar base is v0.2.5-test.1, commit\n5445b96713ad1176da173721edd7aa927b29bf1a.\nhttps://github.com/fitzforge/polestar\nAdaptation and support: https://github.com/julen92/SendaFH\n'''

def eligible(p):
    return p.is_file() and not any(x in SKIP for x in p.relative_to(ROOT).parts)

def build(output):
    output.mkdir(parents=True,exist_ok=True)
    addon=ROOT/'addon'
    for name in MODULES:
        toc=addon/name/(name+'.toc')
        assert toc.is_file(),toc
        text=toc.read_text(encoding='utf-8-sig')
        assert f'## Version: {VERSION}' in text,toc
        for line in text.splitlines():
            if line.strip() and not line.lstrip().startswith('#'):
                assert (toc.parent/line.strip().replace('\\','/')).is_file(),(toc,line)
    for xml in addon.rglob('*.xml'):
        for ref in re.findall(r'<(?:Script|Include)\b[^>]*file=["\']([^"\']+)',xml.read_text(encoding='utf-8-sig')):
            assert (xml.parent/ref.replace('\\','/')).is_file(),(xml,ref)
    installer=output/f'SendaFH-{VERSION}.zip'
    preferred=[];runtime=[]
    with zipfile.ZipFile(installer,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in MODULES:
            for p in sorted((addon/name).rglob('*')):
                if eligible(p) and p.suffix.lower() not in SHELL:
                    relative=p.relative_to(addon).as_posix();z.write(p,relative);runtime.append(relative)
        for p in sorted(ROOT.rglob('*')):
            if eligible(p) and p.relative_to(ROOT).parts[0]!='addon' and p.suffix.lower() not in SHELL:
                relative=p.relative_to(ROOT).as_posix();z.write(p,'SendaFH/Source/'+relative);preferred.append(relative)
        z.writestr('SendaFH/Source/README-source.txt',SOURCE_NOTICE)
    source=output/f'SendaFH-{VERSION}-source.zip'
    with zipfile.ZipFile(source,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(ROOT.rglob('*')):
            if eligible(p):z.write(p,'SendaFH-source/'+p.relative_to(ROOT).as_posix())
    for p in (installer,source):
        with zipfile.ZipFile(p) as z:assert z.testzip() is None,p
    with zipfile.ZipFile(installer) as z:
        names=z.namelist()
        assert {n.split('/')[0] for n in names}==set(MODULES)
        assert not any(Path(n).suffix.lower() in SHELL for n in names)
        assert not any(n.startswith('Polestar') for n in names)
        assert 'SendaFH/Source/locales/esES-guides.json' in names
        assert 'SendaFH/Source/tools/sendafh-curseforge.py' in names
        assert 'SendaFH/Source/LICENSE' in names
    sums=''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in (installer,source))
    (output/'SHA256SUMS.txt').write_text(sums,encoding='utf-8')
    result={'version':VERSION,'modules':list(MODULES),'runtime_files':len(runtime),'editable_source_files':len(preferred)+1,'source_in_installer':'SendaFH/Source/','shell_scripts_in_installer':False,'archives':[{'name':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (installer,source)]}
    (output/'paquete-validacion.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    build(parser.parse_args().output.resolve())
