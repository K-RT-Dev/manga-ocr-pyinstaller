# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import copy_metadata

datas = []
# datas += collect_data_files('torch') # This step can be skipped to reduce the final size of the build
datas += collect_data_files('unidic_lite')
datas += collect_data_files('manga_ocr')
datas += copy_metadata('torch')
datas += copy_metadata('tqdm')
datas += copy_metadata('regex')
datas += copy_metadata('requests')
datas += copy_metadata('packaging')
datas += copy_metadata('filelock')
datas += copy_metadata('numpy')
datas += copy_metadata('tokenizers')

#Here we should list the static files that we want to include in the final build, indicating the source and destination directory
added_files = [
  ('./img', './img')
]

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas + added_files,
    hiddenimports=[], # We should normally specify 'pytorch' as a hidden import, but we can ignore it to reduce the size of the final build
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# This step helps us to ignore several .dll and .lib files that are not necessary in the final build, reducing its size
PATH_TO_TORCH_LIB = "torch\\lib\\"
excluded_files  = [
  'asmjit.lib', 
  'c10.lib',
  'clog.lib',
  'cpuinfo.lib',
  'dnnl.lib',
  'caffe2_detectron_ops.dll',
  'caffe2_detectron_ops.lib',
  'caffe2_module_test_dynamic.dll',
  'caffe2_module_test_dynamic.lib',
  'caffe2_observers.dll',
  'caffe2_observers.lib',
  'Caffe2_perfkernels_avx.lib',
  'Caffe2_perfkernels_avx2.lib',
  'Caffe2_perfkernels_avx512.lib',
  'fbgemm.lib',
  'kineto.lib',
  'libprotobuf-lite.lib',
  'libprotobuf.lib',
  'libprotoc.lib',
  'mkldnn.lib',
  'pthreadpool.lib',
  'shm.lib',
  'torch.lib',
  'torch_cpu.lib',
  'torch_python.lib',
  'XNNPACK.lib',
  '_C.lib'
]
excluded_files = [PATH_TO_TORCH_LIB + x for x in excluded_files]
a.datas = [x for x in a.datas if not x[0] in excluded_files]

# Here we should specify the Python packages that we only use for the development process, so they are not included in the final build
exclude = ["pastel", "tomli", "poethepoet"]
a.binaries = [x for x in a.binaries if not x[0].startswith(tuple(exclude))]

# This Pyinstaller implementation generates the final build not as a single .exe, but as a directory with separate dependencies
# This helps to reduce the startup time when running the .exe
# If we need to put everything in a single file, we can use WinRar to generate an installer
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MangaOcrPyInstaller',
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
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MangaOcrPyInstaller',
)
