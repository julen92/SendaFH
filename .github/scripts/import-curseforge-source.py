"""One-time import of the exact eight modules submitted to CurseForge."""
from pathlib import Path, PurePosixPath
import hashlib, io, os, subprocess, urllib.request, zipfile, json

ROOT=Path(__file__).resolve().parents[2]
assert os.environ.get('GITHUB_REPOSITORY')=='julen92/SendaFH'
assert not (ROOT/'addon/SendaFH/Core/Init.lua').exists(), 'Sources already imported; do not overwrite later changes.'
URL='https://edge.forgecdn.net/files/9208/399/SendaFH-0.5.0-beta.1.zip'
SHA256='b02eaac76ed2a9f05da7af3fc5df910d81f6786a16a4fdf19fc1da117a6c6cff'
with urllib.request.urlopen(URL,timeout=120) as response: payload=response.read()
assert hashlib.sha256(payload).hexdigest()==SHA256, 'Archive SHA256 differs from the submitted package.'
z=zipfile.ZipFile(io.BytesIO(payload)); assert z.testzip() is None
modules={'SendaFH','SendaFH_Guides','SendaFH_ItemDB','SendaFH_QuestDB','SendaFH_Codex','SendaFH_Nav','SendaFH_Names_esES','SendaFH_Names_esMX'}
files={}
for name in z.namelist():
    if name.endswith('/'): continue
    assert name.split('/')[0] in modules
    rel=name[len('SendaFH/Source/'):] if name.startswith('SendaFH/Source/') else 'addon/'+name
    parts=PurePosixPath(rel).parts
    assert parts and '..' not in parts and not PurePosixPath(rel).is_absolute()
    if rel=='README-source.txt':continue
    files[rel]=z.read(name)

def preserved(rel):
    return rel.startswith(('.github/','docs/sendafh/')) or rel in {'README.md','CONTRIBUTING.md','package.json','.gitignore'}

tracked=subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
for rel in tracked:
    if rel and rel not in files and not preserved(rel):
        target=ROOT/rel
        assert target.resolve().is_relative_to(ROOT.resolve())
        if target.is_file():target.unlink()
for rel,content in files.items():
    if preserved(rel):continue
    target=ROOT/rel
    assert target.resolve().is_relative_to(ROOT.resolve())
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(content)

template=ROOT/'docs/sendafh/README-after-import.md'
(ROOT/'README.md').write_bytes(template.read_bytes())
template.unlink()
assert {p.name for p in (ROOT/'addon').iterdir() if p.is_dir()}==modules
for name in modules:
    assert (ROOT/'addon'/name/(name+'.toc')).exists()
runtime_count=0
for rel,content in files.items():
    if rel.startswith('addon/'):
        assert (ROOT/rel).read_bytes()==content, rel
        runtime_count+=1
result={'version':'0.5.0-beta.1','installer_sha256':SHA256,'modules':sorted(modules),'runtime_files_verified':runtime_count,'editable_source_files':sum(not p.startswith('addon/') for p in files),'runtime_matches_submitted_zip':True}
(ROOT/'docs/sendafh/SOURCE-PROVENANCE.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
