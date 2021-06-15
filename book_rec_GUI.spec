# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

add_files = [('C:\\Users\\JOON\\Documents\\python_project\\book_recommend\\extract_data_add_score.csv', '.'),
	   ('C:\\Users\\JOON\\Documents\\python_project\\book_recommend\\tf-idf_matrix.npz', '.'),
	   ('C:\\Users\\JOON\\Documents\\python_project\\book_recommend\\stopwords.csv', '.')
	   ]

a = Analysis(['book_rec_GUI.py'],
             pathex=['C:\\Users\\JOON\\Documents\\python_project\\book_recommend'],
             binaries=[],
             datas=add_files,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='book_rec_GUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
