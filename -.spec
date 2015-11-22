# -*- mode: python -*-
a = Analysis(['-', 'main.py'],
             pathex=['C:\\Users\\Alick\\Dropbox\\Important\\Projects\\Programming\\Python\\AGEye'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='-.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='icon.ico')
