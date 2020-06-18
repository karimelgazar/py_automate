# import os
# LINUX_SYSTEM = 'posix'
# WINDOWS_SYSTEM = 'nt'
# print(os.name == LINUX_SYSTEM)
#! https://stackoverflow.com/a/1325587/9406862

from subprocess import Popen as pop
import subprocess
import os
from tkinter import filedialog, Tk


#! https://stackoverflow.com/a/4760517/9406862
#! https://help.gnome.org/users/zenity/stable/file-selection.html.en
# f = subprocess.run('zenity --file-selection --multiple'.split(),
#                    stdout=subprocess.PIPE, shell=True)


def covert_icons(files, to='.png'):
    # os.chdir(path)
    # files = os.listdir(path)
    for file in files:
        # if os.path.isdir(file):
        #     print(file)
        #     covert_icons(path + '/' + file)

        # if not file.endswith('.ico'):
        #     continue

        # print('\n', file, '-'*50, sep='\n')
        folder_name = os.path.dirname(file)
        hidden_file_name = '.' + os.path.basename(file)[:-4]
        file_name = folder_name + '/' + hidden_file_name + to
        print(file_name)
        try:
            subprocess.getoutput(
                f"convert \"{file}\" -alpha on -background -flatten none \"{file_name}\"")
        except:
            print('failed')


# Tk().withdraw()
# path = filedialog.askdirectory()
ff = subprocess.getoutput("find /home/km/AA_ME | grep \".ico\$\"")


# print(
#     ff.split('\n')
#     # f.stdout.decode('utf-8')
#     # , shell=True)
# )
covert_icons(ff.split('\n'))
