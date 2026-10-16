#!/usr/bin/env python3
"""Package the verified SendaFH 0.2.3 release with the SendaFH overlay.
Modified by Forever Hispano, 2026-10-16. GPL-3.0-only.
"""
from pathlib import Path
import hashlib, shutil, subprocess, zipfile, re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent / 'senda-entrega'
UPSTREAM = OUT / 'SendaFH-0.2.3.zip'
STAGE = OUT / 'instalable'
EXPECTED = '8f6605cf9f40ffa0421f0f046c3c58e38e5f5d360f3830663a91a82b69488c0c'
assert hashlib.sha256(UPSTREAM.read_bytes()).hexdigest() == EXPECTED
STAGE.mkdir(exist_ok=True)
with zipfile.ZipFile(UPSTREAM) as z:
    assert z.testzip() is None
    z.extractall(STAGE)
shutil.copytree(ROOT / 'addon/SendaFH', STAGE / 'SendaFH', dirs_exist_ok=True)
for name in ['LICENSE', 'LICENSE-EXCEPTION.md', 'THIRD_PARTY.md']:
    shutil.copy2(ROOT / name, STAGE / 'SendaFH' / name)
(STAGE / 'SendaFH/Licenses').mkdir(exist_ok=True)
shutil.copy2(ROOT / 'tools/media/fonts/Cinzel-OFL.txt', STAGE / 'SendaFH/Licenses/Cinzel-OFL.txt')

readme = '''SENDA 0.2.0-beta · FOREVER HISPANO
16 de octubre de 2026

INSTALAR
1. Cierra WoW por completo.
2. Abre la carpeta del cliente de WoW Forever que estés usando.
3. Extrae las cinco carpetas de este ZIP dentro de Interface/AddOns:
   SendaFH, SendaFH_Guides, SendaFH_ItemDB, SendaFH_QuestDB y SendaFH_Codex.
   Ejemplo: Interface/AddOns/SendaFH/SendaFH.toc.
   No metas todas ellas dentro de otra carpeta llamada SendaFH.
4. Si ya tienes SendaFH, guarda una copia de esas cinco carpetas y
   reemplázalas por estas. SendaFH es una adaptación, no una segunda copia
   que se deba instalar junto al SendaFH original.
   No borres el addon ForeverHispano ni tus SavedVariables.
5. Inicia el cliente y activa los cinco módulos en la lista de accesorios.
6. Usa /senda. Para ajustes: /senda ajustes. Créditos: /senda creditos.
7. Si conservas colores de una instalación anterior, usa /senda estilo.
   Este comando cambia el tema sin borrar el progreso.

QUÉ CAMBIA
Azul petróleo, cobre y marfil; nuevo emblema de camino; cabecera sobria;
accesos principales a la derecha; panel lateral izquierdo más amplio;
guía más legible; interfaz parcialmente traducida al español.
Las rutas y buena parte de los datos originales siguen en inglés.

COMPATIBILIDAD Y PRUEBAS
Base estable SendaFH 0.2.3, Interface 16001. Versión SendaFH 0.2.0-beta.
Se conserva el nombre técnico SendaFH para rutas, módulos y partidas.
73 pruebas automatizadas superadas y carga de los cinco módulos con
158 guías en entorno simulado. No probado todavía dentro del cliente WoW.
Esto no garantiza compatibilidad con futuras actualizaciones de la beta.
Si aparece un error, comparte el texto completo y los pasos que lo causan.

CRÉDITOS Y CÓDIGO
Adaptación visual y traducción: Forever Hispano.
Basado en Polestar de fitzforge y sus colaboradores:
https://github.com/fitzforge/polestar
Base: v0.2.3, commit 370fe90ef725d58ca5d6ca783689d6f808bcba3e.
Código: GPL-3.0-only. Conserva LICENSE, LICENSE-EXCEPTION.md,
THIRD_PARTY.md y las licencias de datos y fuentes de cada módulo.
El código Lua está disponible directamente en las carpetas del addon.
SendaFH/Source/SendaFH-0.2.0-source.zip incluye el proyecto modificado,
las herramientas de generación de los gráficos y las fuentes de las guías.
No es un producto oficial de Blizzard ni una versión oficial de SendaFH.
'''
(STAGE / 'SendaFH/SENDA-LEEME.txt').write_text(readme)
changed = subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT, text=True).splitlines()
(STAGE / 'SendaFH/SENDA-CAMBIOS.md').write_text(
    '# SendaFH 0.2.0-beta — 2026-10-16\n\n' + readme + '\n\nArchivos modificados respecto a v0.2.3:\n' +
    '\n'.join('- ' + p for p in changed) + '\n\nAñadidos: Core/SendaFH.lua, Core/SendaES.lua, tests/senda.test.js, tools/senda-preview.js y tools/senda-package.py.\n')

# Preserve upstream's distribution gate for generated Codex data.
subprocess.run(['node', '-e', "const {releaseRefusal}=require('./tools/lib/codex/pack'); const r=releaseRefusal(process.argv[1]); if(r)throw new Error(r);", str(STAGE / 'SendaFH_Codex')], cwd=ROOT, check=True)
lua_files = list(STAGE.rglob('*.lua'))
for p in lua_files:
    subprocess.run(['/tmp/senda-lua/lua-5.1.5/src/luac', '-p', str(p)], check=True)
for p in list(STAGE.rglob('*.toc')) + list(STAGE.rglob('*.xml')):
    content = p.read_text(encoding='utf-8-sig')
    refs = ([s.strip() for s in content.splitlines() if s.strip() and not s.lstrip().startswith('#')]
            if p.suffix == '.toc' else re.findall(r'<(?:Script|Include)\b[^>]*file=[\"\']([^\"\']+)', content))
    for ref in refs:
        assert (p.parent / ref.replace('\\', '/')).is_file(), (p, ref)

source_dir = STAGE / 'SendaFH/Source'
source_dir.mkdir(exist_ok=True)
source = source_dir / 'SendaFH-0.2.0-source.zip'
tracked = subprocess.check_output(['git', 'ls-files'], cwd=ROOT, text=True).splitlines()
extras = ['addon/SendaFH/Core/SendaFH.lua', 'addon/SendaFH/Core/SendaES.lua', 'tests/senda.test.js', 'tools/senda-preview.js', 'tools/senda-package.py']
with zipfile.ZipFile(source, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for rel in sorted(set(tracked + extras)):
        p = ROOT / rel
        if p.is_file() and not rel.startswith('addon/'):
            z.write(p, 'SendaFH-source/' + rel)
    for p in sorted(STAGE.rglob('*')):
        if p.is_file() and source_dir not in p.parents:
            z.write(p, 'SendaFH-source/addon/' + str(p.relative_to(STAGE)))
    z.writestr('SendaFH-source/SENDA-LEEME.txt', readme)
    z.writestr('SendaFH-source/UPSTREAM-SHA256.txt', EXPECTED + '  SendaFH-0.2.3.zip\n')
archive = OUT / 'SendaFH-0.2.0-beta.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for p in sorted(STAGE.rglob('*')):
        if p.is_file():
            z.write(p, p.relative_to(STAGE))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    print('Modules:', sorted({p.split('/')[0] for p in z.namelist()}))
print('Lua files checked:', len(lua_files))
print('Installable:', archive, archive.stat().st_size, 'bytes')
print('SHA256:', hashlib.sha256(archive.read_bytes()).hexdigest())
