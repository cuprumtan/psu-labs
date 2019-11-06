# -*- mode: python -*-

block_cipher = None


a = Analysis(['app.py'],
             pathex=['/home/cuprumtan/Desktop/git/circuit-engineering-testing-app'],
             binaries=[],
             datas=[('templates', 'templates'), ('static', 'static'), ('circuit-engineering.db', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='circuit-engineering-testing-app-1.0.1',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='circuit-engineering-testing-app-1.0.1')
