#!/usr/bin/env python3
"""Build the SendaFH install and corresponding-source archives after tests."""
from pathlib import Path
import argparse,hashlib,re,subprocess,zipfile

ROOT=Path(__file__).resolve().parents[1]
VERSION='0.5.0-beta.1'
MODULES={'SendaFH','SendaFH_Guides','SendaFH_ItemDB','SendaFH_QuestDB','SendaFH_Codex','SendaFH_Nav','SendaFH_Names_esES','SendaFH_Names_esMX'}

def package(destination):
    addon=ROOT/'addon'
    subprocess.run(['node',str(ROOT/'tools/senda-build-names.js')],cwd=ROOT,check=True)
    subprocess.run(['node',str(ROOT/'tools/senda-build-guide-locale.js')],cwd=ROOT,check=True)
    subprocess.run(['node',str(ROOT/'tools/senda-locale-audit.js')],cwd=ROOT,check=True)
    subprocess.run(['node',str(ROOT/'tools/senda-guide-audit.js')],cwd=ROOT,check=True)
    subprocess.run(['node',str(ROOT/'tools/sendafh.js'),'nav','check'],cwd=ROOT,check=True)
    subprocess.run(['node','-e',"const {releaseRefusal}=require('./tools/lib/codex/pack');const r=releaseRefusal(process.argv[1]);if(r)throw Error(r);",str(addon/'SendaFH_Codex')],cwd=ROOT,check=True)
    assert MODULES <= {p.name for p in addon.iterdir() if p.is_dir()}
    for p in list(addon.rglob('*.toc'))+list(addon.rglob('*.xml')):
        content=p.read_text(encoding='utf-8-sig')
        refs=([s.strip() for s in content.splitlines() if s.strip() and not s.lstrip().startswith('#')]
              if p.suffix=='.toc' else re.findall(r'<(?:Script|Include)\b[^>]*file=[\"\']([^\"\']+)',content))
        for ref in refs:assert (p.parent/ref.replace('\\','/')).is_file(),(p,ref)
    destination.mkdir(parents=True,exist_ok=True)
    source=destination/f'SendaFH-{VERSION}-source.zip'
    archive=destination/f'SendaFH-{VERSION}.zip'
    with zipfile.ZipFile(source,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(ROOT.rglob('*')):
            if p.is_file() and not any(s in {'.git','node_modules','__pycache__','Source'} for s in p.relative_to(ROOT).parts):
                z.write(p,'SendaFH-source/'+p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in sorted(MODULES):
            for p in sorted((addon/name).rglob('*')):
                if p.is_file() and 'Source' not in p.relative_to(addon).parts:z.write(p,p.relative_to(addon).as_posix())
    for p in (archive,source):
        with zipfile.ZipFile(p) as z:
            assert z.testzip() is None
            if p==archive:
                assert {n.split('/')[0] for n in z.namelist()}==MODULES
                assert not any('polestar' in n.lower() for n in z.namelist())
        print(p)
        print('Bytes:',p.stat().st_size,'SHA256:',hashlib.sha256(p.read_bytes()).hexdigest())

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    package(parser.parse_args().output.resolve())
