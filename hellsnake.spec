# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['hell_snake.py'],
    pathex=['C:\Projects\hell_snake - Stable'],
    binaries=[],
    datas=[
        ('src/res/icons', 'src/res/icons'),
        ('src/res/fonts', 'src/res/fonts'),
        ('src/res/stratagems.json', 'src/res')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='hell_snake',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='src/res/icons/hell_snake.png',
)
