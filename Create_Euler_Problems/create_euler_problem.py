from bs4 import BeautifulSoup
import requests
import os
import sys
import argparse

BASE_LINK = 'https://projecteuler.net/problem='

# the text place holders to replace with
# the problem title & description in the .ipynb file
TO_FILL_PT = '**PROBLEM_TITLE**'
TO_FILL_PC = '\"**PROBLEM_CONTENT**\"'

# change directory to the script path
# so we can find "jupyter_template.json" file
os.chdir(sys.path[0])
template = open('jupyter_template.json')

# so we can create folders & files
os.chdir('e:/karim/Projects/# Youtube/Project_Euler')


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
        print(folder_title)
        print('=' * 50, '\n')
    except:
        print("{} already exists!".format(folder_title).title())
        print('=' * 50, '\n')
        return

    os.chdir(folder_title)
    problem_title = folder_title[len(problem_number):].strip()

    # ? create the .py file
    make_python(problem_number, problem_title, problem_description)
    # ? create the .ipynb file
    make_jupyter(problem_number, problem_title, problem_description)

    os.chdir('..')  # ? return back to the project base folder


parser = argparse.ArgumentParser()
arg_help = '''
        Make a folder for a given problem number 
        >>> OR <<<
        If passed as (:problem_number) make folders until this given problem number (inclusive)'''

parser.add_argument('problem',
                    help=arg_help)

args = vars(parser.parse_args())

problem_number = args['problem']

if problem_number[0] == ':':
    # ? exclude these 3:
    #  1- .git hidden folder
    #  2- .gitignore file
    #  3- Open_Jupyter.py
    last_problem = len(os.listdir()) - 3

    for number in range(last_problem + 1, int(problem_number[1:]) + 1):
        create_folder_for_problem(number)

else:
    create_folder_for_problem(problem_number)
