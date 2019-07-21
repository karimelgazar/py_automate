import os
import re
import pyperclip

# ?6 if any copies were found for this file
foundBefore = 0

# ? create the new name for the file using regex
# ** @param (name) the old name of the file
# ** @param (copiesexist) the number of copies of this files
# ** passed to this function the default value is zero copies


def new_name_of(name, copiesexist=0):
    if name != '':
        print(name)
        rex = re.compile(r'''
                    (S\d{2}(\.)?E(p)?\d{2})         # Get the episode and season number
                    (.*)?                           # The text between the episode number and the videos extension
                    (\.\w+)$''',                    # The video extension
                         re.VERBOSE)
        found = rex.search(name)
        new = ''
        if copiesexist == 0:
            new = found.group(1)+found.group(5)
        else:
            new = found.group(1)+('(%s)' % copiesexist) + found.group(5)
        print(new)
        return new

# ? this function goes through all the files and folders found
# ** in the @param (dir) which refers to the main directory
# ** of all files that need to be renamed

#!! THIS FUNCTION RENAMES ONLY RENAME SERIES WITH
#!! TITLES CONTAIN (EP) AND (SE) FOR ARABIC TITLES
#!! USE FUNCTION rename_all_ar()


def rename_all_en(dir):
    global foundBefore

    if('Prison Break S05') in dir:
        return

    isfile = os.path.isfile(dir)

    if isfile:
        basename = os.path.basename(dir)
        dirname = os.path.dirname(dir)
        new_dir = os.path.join(dirname, new_name_of(basename))
        try:
            os.rename(dir, new_dir)
        except:
            #! there was an error because the program tries to rename a file
            #! to the same name of already existing file (which was renamed earlier)
            foundBefore += 1
            new_dir = os.path.join(dirname, new_name_of(basename, foundBefore))
            os.rename(dir, new_dir)

    else:
        for filename in os.listdir(dir):
            path = os.path.join(dir, filename)
            rename_all_en(path)


def rename_all_ar(dir):
    for file in os.listdir(dir):
        old = file
        print(file)
        file = file.split('(')[1][7:10].strip()
        if ')' in file:
            file = file.replace(')', ' ').strip()

        if int(file) < 10:
            file = '0%s' % file

        os.rename(old, '%s.mp4' % file)
        print('='*20)


dir = pyperclip.paste().replace('\"', '')
# rename_all_ar()
# rename_all_en(dir)
print(' Done '.center(66, '='))
