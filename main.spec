# -*- mode: python ; coding: utf-8 -*-
# from PyInstaller import Analysis, PYZ, EXE, COLLECT

a = Analysis(
    ['advanced_self_diagnosis\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('app.png', '.'), ('app.ico', '.'), ('advanced_self_diagnosis/mitm_log_target.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Paperback Self-Diagnosis Tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Paperback Self-Diagnosis Tool',
)
