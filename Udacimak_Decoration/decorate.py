import argparse
import webbrowser
import os
import sys


SCRIPT_BASE_PATH = sys.path[0]
decoration = open(SCRIPT_BASE_PATH + '/decoration.html', 'r').read()
folders = []


def html_files_in(dirctory):
    return sorted([x for x in os.listdir(dirctory) if x.endswith(
        '.html') and not x.startswith('index')])


def decorate(html_file, files, dirctory):
    """
    THIS METHOD: adds decoration to the html files
    you sholud edit the decoration.html file
    to add a new decoration to the html

    Arguments:
    =========
        html_file  -- the html file to edit
        files  -- all html files in this folder
    """
    global decoration, folders

    previous_button = ''
    next_button = ''
    indx = files.index(html_file)
    folder_indx = folders.index(dirctory)
    scrollbar_index = indx + 1

    if indx >= 0:
        if indx == 0 and folder_indx > 0:  # the previous lesson button
            pre_dirctory = folders[folder_indx - 1]
            folder_name = os.path.basename(pre_dirctory)
            file = html_files_in(pre_dirctory)[-1]
            previous_button = "<a href=\"../{}/{}\" class=\"btn btn-warning\" role=\"button\" style=\"font-size : 50px; width: 100%; height: 75%px;background-color: #007bff;\">Previous Lesson 🤖</a>".format(
                folder_name, file)

        if indx < len(files) - 1:  # normal next concept button
            next_button = "<a href=\"{}\" class=\"btn btn-success\" role=\"button\" style=\"font-size : 50px; width: 100%; height: 75%px;\">Next Concept ⚡|🐱‍💻</a>".format(
                files[indx + 1])

    if indx < len(files):
        if (indx == (len(files) - 1)) and (folder_indx < (len(folders) - 1)):  # the next lesson button
            next_dirctory = folders[folder_indx + 1]
            folder_name = os.path.basename(next_dirctory)
            file = html_files_in(next_dirctory)[0]
            next_button = "<a href=\"../{}/{}\" class=\"btn btn-success\" role=\"button\" style=\"font-size : 50px; width: 100%; height: 75%px;background-color: #007bff;\">Next Lesson 🐱‍🏍</a>".format(
                folder_name, file)

        if indx > 0:
            previous_button = "<a href=\"{}\" class=\"btn btn-warning\" role=\"button\" style=\"font-size : 50px; width: 100%; height: 75%px;\">Previous Concept 🔍|🚀</a>".format(
                files[indx - 1])

    # if ascii errors occured when
    #  encoding to UTF-8 just ignore them
    old = open(html_file, "r", encoding="UTF-8", errors='ignore').readlines()

    with open(html_file, "w", encoding="UTF-8", errors='ignore') as new:
        for line in old:
            # this is so important you should use
            # </main> so that you can add new features freely
            # and not to affect the page original source code
            if '</main>' in line:
                new.write(line)  # write this line

                # add the decoration
                new_decoration = decoration.replace('XX1', next_button)
                new_decoration = new_decoration.replace('XX2', previous_button)

                new.write(new_decoration.replace('XX3', str(scrollbar_index)))
                print("Done With File: {}".format(html_file))
                return
            else:
                new.write(line)


def extract_html_in(dirctory):

    print(dirctory)
    print('=' * 30)

    os.chdir(dirctory)
    htmls = html_files_in(dirctory)
    for html in htmls:
        decorate(html, htmls, dirctory)

    print('this folder is finished\n'.title())


def pick_course(path):
    global folders

    # ? a folder for a single module was given not the whole course
    if 'Part' in path:
        extract_html_in(path)
        return

    else:  # ? the whole course was given
        folders = [os.path.join(path, item) for item in os.listdir(
            path) if item.startswith('Part')]
        for folder in folders:
            extract_html_in(folder)


# ==============================================
# ? THE SCRIPT STARTS EXCUTING FROM HERE
# ==============================================
#! get the course folder
parser = argparse.ArgumentParser()
help_1 = '[REQUIRED]: The Course Folder'

parser.add_argument('course_folder',  help=help_1)

COURSE_FOLDER = parser.parse_args().course_folder
COURSE_FOLDER = os.path.abspath(COURSE_FOLDER)
pick_course(COURSE_FOLDER)

home_page = os.path.join(COURSE_FOLDER, 'index.html')

if os.path.exists(home_page):
    webbrowser.open(home_page)

# if more_than_one:
#     for course in os.listdir(path):
#         full_path = os.path.join(path, course)

#         if os.path.isdir(full_path):
#             pick_course(full_path)
# else:
#     pick_course(path)
