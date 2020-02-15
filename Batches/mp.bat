@python "E:/karim/Py_Automate/merge_pdfs.py"
IF ERRORLEVEL 1 PAUSE && EXIT

import PyPDF2
import os
import webbrowser
from tkinter import filedialog, Tk

LINE_SEP = '='*80
pdfFiles = []

many_or_2 = input(
    'please input:\n0 >>> for 2 pdfs to combine\nor\nany key >>> to merge many pdfs.\n:'.title())


def pick_output_folder():
    """
    This method launch a folder picker to choose
    the root output folder
    """
    where_to = ''
    while not where_to:
        # Pick output folder
        print(LINE_SEP, end='')
        print('\nplease choose where to output the PDF.'.upper())
        print(LINE_SEP)
        Tk().withdraw()  # to hide the small tk window
        where_to = filedialog.askdirectory()  # folder picker

    return where_to


def pick_pdf_file():
    """
    This method launch a folder picker to choose
    the folder of the pdf to append
    """
    from_where = ''
    while not from_where or not from_where.endswith('.pdf'):
        # Pick download folder
        Tk().withdraw()  # to hide the small tk window
        from_where = filedialog.askopenfilename()  # folder picker

    return from_where


if(many_or_2 == '0'):  # 2 pdfs
    print(LINE_SEP, end='')
    print('Please choose the main Pdf.'.title())
    print(LINE_SEP)

    main_pdf = pick_pdf_file()
    pdfFiles.append(main_pdf)

    print()
    print(LINE_SEP, end='')
    print('Please choose the second Pdf.'.title())
    print(LINE_SEP)

    second_pdf = pick_pdf_file()
    pdfFiles.append(second_pdf)

    output_pdf_path = pick_output_folder() + os.path.basename(main_pdf)

else:  # many pdfs
    print(LINE_SEP, end='')
    print('\nPlease Choose The Folder That Contains The PDFs.')
    print(LINE_SEP)

    Tk().withdraw()
    from_where = filedialog.askdirectory()  # folder picker
    os.chdir(from_where)
    pdfFiles = [x for x in os.listdir() if x.endswith('.pdf')]
    output_pdf_path = pick_output_folder() + 'Grouped ' + pdfFiles[0]


print(LINE_SEP, 'Merging Pages...', LINE_SEP, sep='\n')
pdfWriter = PyPDF2.PdfFileWriter()

for filename in pdfFiles:
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pdfWriter.appendPagesFromReader(pdfReader)

pdfOutput = open(output_pdf_path, 'wb')
pdfWriter.write(pdfOutput)
pdfOutput.close()

print('Done.')
webbrowser.open(output_pdf_path)
