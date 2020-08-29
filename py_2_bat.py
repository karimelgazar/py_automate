import os
from tkinter import filedialog, Tk

BASE_DIR = "/home/km/karim/py_automate"

Tk().withdraw()
files = filedialog.askopenfilenames()

for file in files:
    print("THE FILE:", file)
    py_name = os.path.basename(file)

    if py_name == '00-startup.py':
        continue

    bat_name = "".join([i[0] for i in py_name.split('_')])
    bat_name = "{}\Batches\{}.bat".format(BASE_DIR, bat_name)

    with open(bat_name, 'w', encoding="UTF-8") as bat:
        bat.write("@python \"{}\" %*\n".format(file))

    print(bat_name)
