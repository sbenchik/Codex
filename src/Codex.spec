# -*- mode: python -*-

block_cipher = None


a = Analysis(['Codex'],
             pathex=['/home/steve/Documents/Projects/Python/Codex/src'],
             binaries=[],
             datas=[('icons/256x256/codex.png','icons'), ('bee_movie.txt','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Codex',
          debug=False,
          strip=False,
          upx=True,
          console=True )
