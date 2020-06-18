from tkinter import Tk, filedialog
import os
import webbrowser

LINE_SEP = '-' * 50


def pick_file():
    """
    تقوم الدلة بفتح نافذة لاختيار المجلد المراد
    كتابة اسماء كحتوياته فى ملف نصى
    """
    where_to = ''
    while not where_to:
        # اختار المجلد
        print('\nplease choose the file.'.upper())
        print(LINE_SEP)
        Tk().withdraw()  # حتى لا تظهر نوافذ اخرى
        where_to = filedialog.askopenfilename()  # نافذة اختيار المجلد

    return where_to


def create_file(original_file):
    """
    تقوم الدلة بكتابة محتويات المجلد المعطى 
    فى ملف نصى
    """
    # اسم الملف
    new_file_name = 'no-version-' + os.path.basename(original_file)
    folder_path = os.path.dirname(original_file)

    # المسار الكامل للملف داخل المجلد المختار
    full_path_txt = os.path.join(folder_path, new_file_name)

    # كتابة محتويات المجلد
    with open(full_path_txt, encoding='UTF-8', mode='w') as new_file:
        with open(original_file, encoding='UTF-8', mode='r') as original:
            for line in original.readlines():
                equal_sign = line.find('=')
                new_file.write(line[:equal_sign])

    return full_path_txt


########################################################
# ? البرنامج يبدأ هنا
########################################################
txt_path = create_file(pick_file())

webbrowser.open(txt_path)  # افتح الملف عند الانتهاء
