# -*- mode: python ; coding: utf-8 -*-

added_files = [
    ("../scripts/qt/ui/transcription_main_window.ui", "ui/."),
    ("../scripts/qt/qss/dark.qss", "qss/."),
    ("../scripts/qt/qss/dark_icons", "qss/dark_icons/")
]

a = Analysis(
    ['../scripts/qt/transcriptor_main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='transcriptor_main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='transcriptor_main',
)
