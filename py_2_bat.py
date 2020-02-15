import os
from tkinter import filedialog, Tk

BASE_DIR = "E:\karim\Py_Automate"

Tk().withdraw()
files = filedialog.askopenfilenames()

for file in files:
    print("THE FILE:", file)
    with open(file, 'r', encoding="UTF-8") as py:
        py_name = os.path.basename(file)

        if py_name == '00-startup.py':
            continue

        bat_name = "".join([i[0] for i in py_name.split('_')])
        bat_name = "{}\Batches\{}.bat".format(BASE_DIR, bat_name)

        with open(bat_name, 'w', encoding="UTF-8") as bat:
            bat.write("@python \"{}\"\n".format(file))
            bat.write("IF ERRORLEVEL 1 PAUSE && EXIT\n\n")
            bat.write(py.read())

        print(bat_name)
