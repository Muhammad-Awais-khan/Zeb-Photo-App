# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# Collect all data/binaries for rembg and onnxruntime
rembg_datas, rembg_binaries, rembg_hiddenimports = collect_all('rembg')
onnx_datas, onnx_binaries, onnx_hiddenimports = collect_all('onnxruntime')

a = Analysis(
    ['src\\app.py'],
    pathex=[],
    binaries=rembg_binaries + onnx_binaries,
    datas=[
        ('src\\bg.jpeg', '.'),
        ('src\\haarcascade_frontalface_default.xml', '.'),
        ('src\\icon.ico', '.')
    ] + rembg_datas + onnx_datas,
    hiddenimports=[
        'cv2',
        'numpy',
        'reportlab',
        'PIL'
    ] + rembg_hiddenimports + onnx_hiddenimports,
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
    a.binaries,
    a.datas,
    [],
    name='ZebPhotoApp',
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
    icon='src\\icon.ico',
)
