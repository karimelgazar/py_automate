from tkinter import Tk, filedialog
import sys
import os
import webbrowser

LINE_SEP = '-' * 80


def pick_script_file():
    """
    This method launch a folder picker to choose
    the root download folder 
    """
    files = []
    while len(files) < 2:
        # Pick nessecaryfiles
        Tk().withdraw()  # to hide the small tk window

        print('\nplease choose where the script file.'.upper())
        script = filedialog.askopenfilename()  # script picker
        if not script.endswith('.py'):
            print('please choose a correct python script')
            print(LINE_SEP)
            continue
        files.append(script)

        print('\nplease choose where the icon file.'.upper())
        icon = filedialog.askopenfilename()  # icon picker
        print(LINE_SEP)
        while not icon.endswith('.ico'):
            print('please choose a correct icon file')
            icon = filedialog.askopenfilename()  # icon picker
            print(LINE_SEP)

        files.append(icon)

    return files


def pick_output_path():
    """
    This method launch a folder picker to choose
    the root download folder 
    """
    where_to = ''
    while not where_to:
        # Pick download folder
        print('\nplease choose where to put download folder.'.upper())
        print(LINE_SEP)
        # Tk().withdraw()  # to hide the small tk window
        where_to = filedialog.askdirectory()  # folder picker

    return where_to


def start_encoding_exe(files):
    script_path = files[0]
    icon_path = files[1]

    script_name = os.path.basename(script_path)
    base_path = os.path.dirname(script_path)
    output_path = os.path.join(pick_output_path(), script_name[:-3])

    try:
        os.makedirs(output_path)
    except:
        sys.exit()

    spec = """
    
    block_cipher = None

a = Analysis(['%s'],
             pathex=['%s'],
             binaries=[('E:\Progammes\chromedriver_win32', '.')],
             datas=[],
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
          exclude_binaries=True,
          name='createEVIPOrg_Automation_new',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='%s') """ % (script_path, output_path, script_path)

    s = open(os.path.join(output_path, 's.spec'), 'w')
    s.write(spec)
    s.close()

    os.chdir(output_path)
    command = "pyinstaller --onefile -w --icon=%s %s" % (
        icon_path, script_path)
    os.system(command)
    webbrowser.open(output_path)


start_encoding_exe(pick_script_file())
