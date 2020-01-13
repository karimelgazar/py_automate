import os
import webbrowser
from tkinter import filedialog, Tk
import os


# TODO ADD a shortcut to collapse the side bar (Alt+b)

# TODO ADD a button to move to the next lesson in the last concept

# TODO ADD a button to move to the previous lesson in the first concept

def decorate(html_file, files):
    """
    THIS METHOD: adds decoration to the html files
    you sholud edit the decoration.html file
    to add a new decoration to the html

    Arguments:
    =========
        html_file  -- the html file to edit
        files  -- all html files in this folder
    """

    decoration = open('decoration.html', 'r').read()

    previous = ''
    next = ''
    indx = files.index(html_file)


   scrollbar_index = indx + 1

   if indx > 0:
        previous = files[indx - 1]

    if indx < (len(files) - 1):
        next = files[indx + 1]

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
                new_decoration = decoration.replace('XX1', next)
                new_decoration = new_decoration.replace('XX2', previous)

                new.write(new_decoration.replace('XX3', scrollbar_index))
                print("Done With File: {}".format(html_file))
                return
            else:
                new.write(line)


def extract_html_in(dirctory):
    if 'Part' in dirctory:
        print(dirctory)
        print('=' * 30)

        os.chdir(dirctory)

        htmls = sorted([x for x in os.listdir(dirctory) if x.endswith(
            '.html') and not x.startswith('index')])
        for html in htmls:
            decorate(html, htmls)
        print('this folder is finished\n'.title())


def pick_course():
  # Pick HTMLs Folder
    Tk().withdraw()  # to hide the small tk window
    path = filedialog.askdirectory()  # folder picker

    for item in os.listdir(path):
        # ? the whole course was given
        item_absolute_path = os.path.join(path, item)
        if os.path.isdir(item_absolute_path):
            extract_html_in(item_absolute_path)

        # ? a folder for a single module was given not the whole course
        else:
            extract_html_in(path)


pick_course()
