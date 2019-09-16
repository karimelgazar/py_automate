import PyPDF2
import os
import webbrowser
from tkinter import filedialog, Tk

LINE_SEP = '-'*80
pdfFiles = []


def pick_output_folder():
    """
    This method launch a folder picker to choose
    the root download folder 
    """
    where_to = ''
    while not where_to:
        # Pick download folder
        print('\nplease choose where to output the PDF.'.upper())
        print(LINE_SEP)
        Tk().withdraw()  # to hide the small tk window
        where_to = filedialog.askdirectory()  # folder picker

    return where_to


def pick_pdf_file():
    """
    This method launch a folder picker to choose
    the root download folder 
    """
    where_to = ''
    while not where_to or not where_to.endswith('.pdf'):
        # Pick download folder
        print('\nplease choose a correct PDF.'.upper())
        print(LINE_SEP)
        Tk().withdraw()  # to hide the small tk window
        where_to = filedialog.askopenfilename()  # folder picker

    return where_to


print('Please choose the main Pdf.'.title())
main_pdf = pick_pdf_file()
pdfFiles.append(main_pdf)

print('Please choose the second Pdf.'.title())
second_pdf = pick_pdf_file()
pdfFiles.append(second_pdf)


pdfWriter = PyPDF2.PdfFileWriter()
print(LINE_SEP, 'Merging Pages', LINE_SEP, sep='\n')

for filename in pdfFiles:
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pdfWriter.appendPagesFromReader(pdfReader)

output_pdf_path = pick_output_folder() + os.path.basename(main_pdf)
pdfOutput = open(output_pdf_path, 'wb')
pdfWriter.write(pdfOutput)
pdfOutput.close()

webbrowser.open(output_pdf_path)
