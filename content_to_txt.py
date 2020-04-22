from tkinter import Tk, filedialog
import os
import webbrowser

LINE_SEP = '-' * 50


def pick_folder():
    """
    تقوم الدلة بفتح نافذة لاختيار المجلد المراد
    كتابة اسماء كحتوياته فى ملف نصى
    """
    where_to = ''
    while not where_to:
        # اختار المجلد
        print('\nplease choose the base folder.'.upper())
        print(LINE_SEP)
        Tk().withdraw()  # حتى لا تظهر نوافذ اخرى
        where_to = filedialog.askdirectory()  # نافذة اختيار المجلد

    return where_to


def create_txt(folder_path):
    """
    تقوم الدلة بكتابة محتويات المجلد المعطى 
    فى ملف نصى
    """
    # اسم الملف
    name_txt = 'content.txt'

    # المسار الكامل للملف داخل المجلد المختار
    full_path_txt = os.path.join(folder_path, name_txt)

    # كتابة محتويات المجلد
    with open(full_path_txt, encoding='UTF-8', mode='w') as txt:
        for item in os.listdir(folder_path):
            print(item, LINE_SEP, sep='\n', file=txt)

    return full_path_txt


########################################################
# ? البرنامج يبدأ هنا
########################################################
txt_path = create_txt(pick_folder())

webbrowser.open(txt_path)  # افتح الملف عند الانتهاء
