from bs4 import BeautifulSoup
import requests
import os
import sys
import argparse
import webbrowser

BASE_LINK = 'https://projecteuler.net/problem='
LINE_SEP = '=' * 50 + '\n'
BASE_PATH = 'e:/karim/Projects/# Youtube/Project_Euler'

# the text place holders to replace with
# the problem title & description in the .ipynb file
TO_FILL_PT = '**PROBLEM_TITLE**'
TO_FILL_PC = '\"**PROBLEM_CONTENT**\"'

# change directory to the script path
# so we can find "jupyter_template.json" file
os.chdir(sys.path[0])
template = open('jupyter_template.json')

# so we can create folders & files
os.chdir(BASE_PATH)


def make_jupyter(problem_number, problem_title, problem_description):
    """
    create the .ipynb file

    Arguments:
        problem_number {str}  
        problem_title {str}  
        problem_description {BeautifulSoup tag} 
    """

    with open('{}.ipynb'.format(problem_number), 'w', encoding="UTF-8") as jupyter:
        for line in template.readlines():  # read the temlplate

            # replace the place holder with the problem title
            if TO_FILL_PT in line:
                jupyter.write(line.replace(TO_FILL_PT, problem_title))

            # replace the place holder with the problem description
            elif TO_FILL_PC in line:
                # markdown does not allow multiple lines to be included
                # in the same double quotes ("") so 'X\nY' should be
                # "X",
                # "Y"
                html = str(problem_description).split('\n')
                for i, code in enumerate(html):
                    # ? this is important because we need to escape
                    # ? the double quotes by finding it through (\")
                    # ? then replacing it by (\\") so that markdown
                    # ? treat it as a (") otherwise errors will happen
                    code = code.replace('\"', '\\"')
                    # as I noticed you must add (\n) before the end quote
                    # to mimic the original html code
                    code = "\"{}\\n\"".format(code)
                    jupyter.write(code)

                    if i != len(html) - 1:  # if not the last line
                        jupyter.write(',\n')

            else:
                jupyter.write(line)


def make_python(problem_number, problem_title, problem_description):
    """
     create the .py file

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
    returns the title and description of a problem given its number

    Arguments:
        problem_number {str}
    """

    # get the html code of the problem
    req = requests.get(BASE_LINK + problem_number)

    # use soup to get the problem title & description
    soup = BeautifulSoup(req.text, "html.parser")
    problem_title = soup.select('#content > h2')[0].text
    problem_description = soup.select('.problem_content')[0]
    folder_title = ' '.join([problem_number, problem_title])

    return(folder_title, problem_description)


def create_folder_for_problem(number):

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

    # ? create the .py file
    make_python(problem_number, problem_title, problem_description)
    # ? create the .ipynb file
    make_jupyter(problem_number, problem_title, problem_description)

    os.chdir('..')  # ? return back to the project base folder


def get_problem_numeber():
    """
    this method returns 
    1)[int] the problem number 
    passed to the script and check if it's valid or not

    2)[int] the number of the last problem already exist 
    to use it to make a group of problems folders
    OR None if a single problem number was given without (:) sign
    """

    # ? Create Argument Parser
    parser = argparse.ArgumentParser()
    arg_help = '''
            Make a folder for a given problem number 
            >>> OR <<<
            If passed as (:problem_number) make folders until this given problem number (inclusive)'''

    parser.add_argument('problem',
                        help=arg_help)

    problem_number = parser.parse_args().problem

    #! ==============================
    #! Check for Extreme Cases
    #! ==============================

    # if invalid input was passed exit because
    # the last char in the string must be an integer
    if not problem_number[-1].isdigit():
        print('\ninvalid input please pass a [number] or [:number]'.title())
        print(LINE_SEP)
        sys.exit()

    # ? craete a grouup of folders
    if problem_number[0] == ':':
        # ? exclude these 3:
        #  1- .git hidden folder
        #  2- .gitignore file
        #  3- Open_Jupyter.py
        last_problem = len(os.listdir()) - 3
        until = int(problem_number[1:])

        if last_problem >= until:
            print('[INFO] all problems folders already exists'.title())
            print(LINE_SEP)
            sys.exit()

        return until, last_problem

    # ? a single problem number was given
    return problem_number, None


########################################################
# ? THE SCRIPT STARTS EXCUTING FROM HERE
########################################################
problem_number, lastest_exist = get_problem_numeber()

if lastest_exist:
    for number in range(lastest_exist + 1, problem_number + 1):
        create_folder_for_problem(number)

else:
    create_folder_for_problem(problem_number)

# when finished open the base folder
webbrowser.open(BASE_PATH)
