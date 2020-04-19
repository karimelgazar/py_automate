from bs4 import BeautifulSoup
import requests
import os
import sys
import argparse
import webbrowser

# تغيير الدليل إلى مسار البرنامج النصي
#  حتى نتمكن من العثور على الملفات
# 1: "jupyter_template.json"
# 2: "problem_folder_path.txt"
os.chdir(sys.path[0])


BASE_LINK = 'https://projecteuler.net/problem='
LINE_SEP = '=' * 50 + '\n'


#! المكان النص الذى سيتم استبداله بــ
#!.ipynb عنوان المشكلة ووصفها في ملف
# ? لم ندرج علامة التنصيص (\")
# ? لأننا نحتاجها لكتابة رأس المشكلة
TO_FILL_PT = '**PROBLEM_TITLE**'

# ? تضمين علامة التنصيص ("\) لأننا نريد استبدالها
# ? وإذا لم نستخدمه ، فإن ملف الجاسون سيعطي خطأ
TO_FILL_PC = '\"**PROBLEM_CONTENT**\"'

template = open('jupyter_template.json', encoding="UTF-8")

BASE_PATH = open("problem_folder_path.txt", 'r',
                 encoding='UTF-8').read().strip()

# وبالتالى يمكننا إنشاء الملفات والمجلدات داخل مجلد المسائل الرئيسى
os.chdir(BASE_PATH)


def make_jupyter(problem_number, problem_title, problem_description):
    """
    تقوم الدالة بانشاء ملف جوبيتر

    Arguments:
        problem_number {str}  
        problem_title {str}  
        problem_description {BeautifulSoup tag} 
    """

    with open('{}.ipynb'.format(problem_number), 'w', encoding="UTF-8") as jupyter:
        for line in template.readlines():  # اقرأ القالب

            # ضع عنوان المشكلة
            if TO_FILL_PT in line:
                jupyter.write(line.replace(TO_FILL_PT, problem_title))

            # ضع وصف المشكلة
            elif TO_FILL_PC in line:
                #!  لا تسمح بوجود كلام متعدد الاسطر داخل نفس اقواس التنصيص markdown
                # ?  يجب ان يكون كالتالى "X\nY" ولذلك
                """
                    "X",
                    "Y"
                """
                html = str(problem_description).split('\n')
                for i, code in enumerate(html):
  
                    #! هذا مهم جدا
                    # ? (\\")نحن نحتاج الى استبدال ("\) بــ
                    # ? (\")حتى تسسطيع بايثون ان تكتبها كـ
                    # ? ان تفهمها markdown وبالتالى تستطيع لغة ال
                    # ? كــ(") والا سيحدث خطأ
                    code = code.replace('\"', '\\"')

                    #! قبل نهاية علامة التنصيص (\n) لقد اكتشقت أنه يجب إضافة
                    #! الأصلي html  لمحاكاة كود
                    code = "\"{}\\n\"".format(code)
                    jupyter.write(code)

                    if i != len(html) - 1:  # اذا لم يكن آخر سطر
                        jupyter.write(',\n')

            else:
                jupyter.write(line)


def make_python(problem_number, problem_title, problem_description):
    """
     تقوم الدالة بانشاء ملف بايثون

    Arguments:
        problem_number {str}  
        problem_title {str}  
        problem_description {BeautifulSoup tag} 
    """
    with open('{}.py'.format(problem_number), 'w', encoding="UTF-8") as py_file:
        print("'''",
              problem_title,
              '=' * 50,
              problem_description.text,
              "'''", sep='\n', file=py_file)


def get_title_desc_of(problem_number):
    """
    تقوم بارجاع عنوان ووصف المسألة باستخدام الرقم المعطى فقط

    Arguments:
        problem_number {str}
    """

    # htmlاستخرج كود الــ
    req = requests.get(BASE_LINK + problem_number)

    # احصل على اعنوان ووصف المسألة
    soup = BeautifulSoup(req.text, "html.parser")
    problem_title = soup.select('#content > h2')[0].text
    problem_description = soup.select('.problem_content')[0]
    folder_title = ' '.join([problem_number, problem_title])

    return(folder_title, problem_description)


def create_folder_for_problem(number):
    """
    تقوم بانشاء مجلد للمسألة باستخدام الرقم المعطى فقط

    Arguments:
        number {int} -- رقم المسألة
    """
    if int(number) <= 0:
        print('\nproblem number must be bigger than zero.'.title())
        print(LINE_SEP)
        sys.exit()

    problem_number = str(number).zfill(3)
    folder_title, problem_description = get_title_desc_of(problem_number)

    try:
        os.mkdir(folder_title)
        print('[CREATED] {}'.format(folder_title))
        print(LINE_SEP)
    except:
        print("[INFO] {} already exists!".format(folder_title).title())
        print(LINE_SEP)
        return

    os.chdir(folder_title)
    problem_title = folder_title[len(problem_number):].strip()

    # ? انشاء ملف بايثون
    make_python(problem_number, problem_title, problem_description)
    # ? انشاء ملف جوبيتر
    make_jupyter(problem_number, problem_title, problem_description)

    os.chdir('..')  # ? ارجع الى مجلد المسائل الأساسى


def extract_number(text):
    """

    استخرج رقم المسائل من النص الذي تم تمريره
    والتحقق مما إذا كان هناك العديد من المسائل لإنشائها أم لا

    Arguments:
        text {str} -- النص المعطى فى الترمينال

    Returns:
        (int(text), many_problems) {tuple} 
    """

    # ? إذا كان هناك العديد من المسائل لإنشائها أم لا
    many_problems = False

    # ? هناك العديد من المسائل لإنشائها
    if text[0] == ':':
        # ? (:)افحص الجزء بعد الــ
        text = text[1:]
        many_problems = True

    if not text.isdigit():
        print('\ninvalid input please pass a [number] or [:number]'.title())
        print(LINE_SEP)
        sys.exit()

    return int(text), many_problems


def get_problem_numeber():
    """
    ترجع هذه الدالة
    1: [int] رقم المشكلة
    تمريره إلى الترمينال والتحقق مما إذا كان صالح 

    2: [int] رقم آخر مسألة موجود بالفعل
    لاستخدامه في إنشاء مجموعة من مجلدات المسائل
    (:)ولا ترجعه إذا تم إعطاء رقم مشكلة واحدة بدون علامة الــ 
    """

    # ? تجهيز الترمينال
    parser = argparse.ArgumentParser()
    arg_help = '''
            Make a folder for a given problem number 
            >>> OR <<<
            If passed as (:problem_number) make folders
            until this given problem number (inclusive)'''

    parser.add_argument('problem',
                        help=arg_help)

    problem_number = parser.parse_args().problem

    problem_number, many_problems = extract_number(problem_number)

    # ? تم اعطاء رقم لمسألة واحدة
    # ? ولذلك لا نحتاج لارجاع رقم اخر مسالة موجودة
    last_problem = None

    # ? انشاء مجموعة من المجلدات
    if many_problems:
        exclude = 1
        folder_content = os.listdir()

        if '.git' in folder_content:
            # ? تجاهل هؤلاء الـثلاثة:
            #  1- .git hidden folder
            #  2- .gitignore file
            #  3- Open_Jupyter.py
            exclude = 3

        last_problem = len(folder_content) - exclude

        if last_problem >= problem_number:
            print('[INFO] all problems folders already exists'.title())
            print(LINE_SEP)
            sys.exit()

    return problem_number, last_problem


########################################################
# ? البرنامج يبدأ هنا
########################################################
problem_number, lastest_exist = get_problem_numeber()

if lastest_exist != None:
    for number in range(lastest_exist + 1, problem_number + 1):
        create_folder_for_problem(number)

else:
    create_folder_for_problem(problem_number)

#! عند الانتهاء قم بفتح المجلد الاساسى
webbrowser.open(BASE_PATH)
