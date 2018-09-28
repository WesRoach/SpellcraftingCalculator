# -*- mode: python -*-

# block_cipher = None

added_datas = [('./interface/*.ui', 'interface'),]

a = Analysis(
    ['Spellcraft.py'],
    binaries = None,
    datas = added_datas,
    hiddenimports = None,
    hookspath = None,
    runtime_hooks = None,
    excludes = None,
    )

pyz = PYZ(
    a.pure,
    a.zipped_data,
    )

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name = 'Spellcraft',
    debug = False,
    upx = True,
    console = True,
    icon = './images/Spellcraft.ico'
    )
