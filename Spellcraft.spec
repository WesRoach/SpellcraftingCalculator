extras = [
    ('./images', 'images'),
    ('./interface/*.ui', 'interface'),
    ('./reports', 'reports'),
    ]

a = Analysis(
    ['Spellcraft.pyw'],
    pathex = None,
    binaries = None,
    datas = extras,
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
