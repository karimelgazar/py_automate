import pyperclip
import pyqrcode
import webbrowser
import os
import sys

ROOT_PATH = 'E:\\karim'
os.chdir(ROOT_PATH)
QR_NAME = "myqr.svg"
LINE_SEP = '%' * 80


def show_qr():
    message = pyperclip.paste()

    # Generate QR Code
    url = pyqrcode.create(message)
    url.svg(QR_NAME, scale=4)

    webbrowser.open(QR_NAME)


print(LINE_SEP)
print('\t\t\tHow To Use\n\t\t', '-' * 25)
print('Enter 0 to exit.'.title(),
      'OR Enter any key to continue'.title(),
      sep='\n')
print(LINE_SEP)

my_input = ''
while my_input != '0':
    show_qr()
    my_input = input('Show Another QR CODE? ')

sys.exit()
