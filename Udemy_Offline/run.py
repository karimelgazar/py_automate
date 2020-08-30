"""
IMPORTANT NOTES
====================

1) The script will choose the first image it faces as the wallpaper iamge inside the course folder

2) The script will modify the original html files but before that the script
    will copy them into files with same name but end with "_original.html".

3) HTML5 specification does not support subtitle format other than webvtt,
    so you need a webvtt format subtitle for the src. so we create will convert
    the srt subtuile to vtt subtitle if the "vtt" subtitle file did not already exists
"""


import argparse
import os
import re
import sys
from distutils.dir_util import copy_tree
from pprint import pprint
import webvtt  # pip install webvtt-py

SCRIPT_PATH = sys.path[0]
LINE_SEP = '='*50
# video title without extension
ITEM_NAME_PLACEHOLDER = '$ITEM_NAME$'
# video title with extension
ITEM_PATH_PLACEHOLDER = '$ITEM_PATH$'
FOLDER_NAME_PLACEHOLDER = '$FOLDER_TITLE$'
SIDEBAR_ITEMS_PLACEHOLDER = '$SIDEBAR_ITEMS$'
PREVIOUS_ITEM_PLACEHOLDER = '$PREVIOUS_ITEM$'
NEXT_ITEM_PLACEHOLDER = '$NEXT_ITEM$'
ITEM_INDEX = '$ITEM_INDEX$'
SUBS_PLACEHOLDER = '$SUBS$'
LESSON_CONTENT = "$LESSON_CONTENT$"
COURSE_TITLE = '$COURSE_TITLE$'
WALPAPER_IMAGE = '$WALPAPER_IMAGE$'

CONTENT_VIDEO = """
<video controls>
  <source src="$ITEM_PATH$" type="video/mp4">
  $SUBS$
</video>
"""

FOLDER_TO_FILES = {}


# ===================================================================
#! get the course folder
parser = argparse.ArgumentParser()
help_1 = '[REQUIRED]: The Course Folder'

parser.add_argument('course_folder',  help=help_1)

COURSE_FOLDER = parser.parse_args().course_folder
# ===================================================================

#! ==============================================
#! make a method to generate the html code by giving it the folder name and videos and subs
#! then use the text returned from this method to replace it in the templeate html file
#! in the calling function
#! ==============================================


def next_prev_items_code(temp, folder_indx, file_indx, list_files):
    global LIST_FOLDERS, FOLDER_TO_FILES
    next_item, prev_item = None, None

    #!======================================
    #! there is one item in the unit
    #!======================================
    if len(list_files) == 1:

        #! there's only one unit
        if len(LIST_FOLDERS) == 1:
            prev_item = next_item = ""

        else:
            #! Next item
            next_folder = LIST_FOLDERS[folder_indx+1]
            next_folder_name = os.path.basename(next_folder)
            first_item_next_unit = list(
                FOLDER_TO_FILES[next_folder].keys())[0]
            first_item_next_unit = os.path.splitext(first_item_next_unit)[0]
            next_item = f"../{next_folder_name}/{first_item_next_unit}.html"

            #! Previous item
            prev_folder = LIST_FOLDERS[folder_indx-1]
            prev_folder_name = os.path.basename(prev_folder)
            last_item_prev_unit = list(
                FOLDER_TO_FILES[prev_folder].keys())[-1]
            last_item_prev_unit = os.path.splitext(last_item_prev_unit)[0]
            prev_item = f"../{prev_folder_name}/{last_item_prev_unit}.html"

    #!======================================
    #! this is the first item
    #!======================================
    elif file_indx == 0:
        next_item = list_files[file_indx + 1]

        #! this is the first unit
        if folder_indx == 0:
            prev_item = ""

        else:
            try:
                prev_folder = LIST_FOLDERS[folder_indx-1]
                prev_folder_name = os.path.basename(prev_folder)
                last_item_prev_unit = list(
                    FOLDER_TO_FILES[prev_folder].keys())[-1]
                last_item_prev_unit = os.path.splitext(
                    last_item_prev_unit)[0]
                prev_item = f"../{prev_folder_name}/{last_item_prev_unit}.html"
            except:
                print()
                print(LINE_SEP)
                print("FROM THIS IS FIRST item")
                print(LIST_FOLDERS[folder_indx],
                      list_files[file_indx], sep='/')
                print(LINE_SEP)
                print()

    #!======================================
    #! this is the last item
    #!======================================
    elif file_indx == len(list_files) - 1:
        prev_item = list_files[file_indx - 1]

        #! this is the last unit
        if folder_indx == len(LIST_FOLDERS) - 1:
            next_item = ""

        else:
            try:
                next_folder = LIST_FOLDERS[folder_indx+1]
                next_folder_name = os.path.basename(next_folder)
                first_item_next_unit = list(
                    FOLDER_TO_FILES[next_folder].keys())[0]
                first_item_next_unit = os.path.splitext(
                    first_item_next_unit)[0]
                next_item = f"../{next_folder_name}/{first_item_next_unit}.html"
            except:
                print()
                print(LINE_SEP)
                print("FROM THIS IS LAST item")
                print(LIST_FOLDERS[folder_indx],
                      list_files[file_indx], sep='/')
                print(LINE_SEP)
                print()
                sys.exit()

    #!===============================================
    #! this is not the first or the last item
    #!===============================================
    else:
        next_item = list_files[file_indx + 1]
        prev_item = list_files[file_indx - 1]

    if prev_item != "":
        prev_item = os.path.splitext(prev_item)[0] + '.html'
    if next_item != "":
        next_item = os.path.splitext(next_item)[0] + '.html'

    #!======================================
    #! PREPROCESSSING...
    #!======================================

    #!===================
    #! NEXT item
    #!===================
    if next_item == "":
        temp = temp.replace(NEXT_ITEM_PLACEHOLDER, "")

    elif next_item.startswith('..'):
        temp = temp.replace(
            NEXT_ITEM_PLACEHOLDER,
            f"<a href=\"{next_item}\" class=\"btn btn-success\" role=\"button\" style=\"font-size : 50px; width: 100%; height: 75%px;background-color: #eb4a5f;\">Next Lesson 👨‍💻 | 🤩</a>"
        )

    else:
        temp = temp.replace(
            NEXT_ITEM_PLACEHOLDER,
            f"<a href=\"{next_item}\" class=\"btn btn-success\" role=\"button\" style=\"font-size : 50px; width: 100%; height: 75%px;\">Next Concept ⚡|🐱‍💻</a>"
        )

    #!===================
    #! PREVIOUS item
    #!===================
    if prev_item == "":
        temp = temp.replace(PREVIOUS_ITEM_PLACEHOLDER, "")

    elif prev_item.startswith('..'):
        temp = temp.replace(
            PREVIOUS_ITEM_PLACEHOLDER,
            f"<a href=\"{prev_item}\" class=\"btn btn-warning\" role=\"button\" style=\"font-size : 50px; width: 100%; height: 75%px;background-color: #7971ea;\">Previous Lesson 🏃</a>"
        )

    else:
        temp = temp.replace(
            PREVIOUS_ITEM_PLACEHOLDER,
            f"<a href=\"{prev_item}\" class=\"btn btn-warning\" role=\"button\" style=\"font-size : 50px; width: 100%; height: 75%px;\">Previous Concept 🔍|🚀</a>"
        )

    return temp


def sidebar_items_code(list_items, are_folders=False):
    items = []

    for item in list_items:
        item_name, item_link = None, None
        if are_folders:
            item_name = os.path.basename(item)
            item_link = f'{item_name}/index'
        else:
            item_name = item_link = os.path.splitext(item)[0]
        items.append(
            f"""
    <li class="">
      <a href="{item_link}.html">{item_name}</a>
    </li>
    """
        )

    #! the element html code
    str_items = '\n'.join(items)

    return str_items


def subs_code(temp, list_subs):
    # the video has no subtitles
    if not list_subs:
        return temp

    #! there's only one sub so it's usually English !!!
    if len(list_subs) == 1:
        # sys.exit(0)
        return temp.replace(
            SUBS_PLACEHOLDER,
            f"<track default=\"true\" kind=\"subtitles\" srclang=\"en\" src=\"{list_subs[0]}\" label=\"en\">"
        )

    all_subs = []
    for i, sub in enumerate(list_subs):
        if i == 0:
            all_subs.append(
                f"<track default=\"true\" kind=\"subtitles\" srclang=\"en\" src=\"{sub}\" label=\"en\">")
            continue

        if '-' in sub:
            lang = sub.split('-')[-1][:2]
            all_subs.append(
                f"<track default=\"false\" kind=\"subtitles\" srclang=\"{lang}\" src=\"{sub}\" label=\"{lang}\">")

    return temp.replace(SUBS_PLACEHOLDER, '\n'.join(all_subs))


# ?==============================================================
# ?                    HTML_LESSON_FILE
# ?==============================================================

def check_if_script_tag_in(html_code):
    """
    this method extracts the url from the script tag of the thml file
    because this script tag ruins every thing and open the external link in the same tab
    HERE'S THE TEMPLATE 
      <script type="text/javascript">window.open("https://github.com/londonappbrewery/Flutter-Course-Resources", '_blank');</script>
    """
    if '</script>' in html_code:
        regex = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"

        url = re.findall(regex, html_code)[0]
        return f"<a href=\"{url}\" target=\"_blank\"><h3>THE LINK</h3> </a>"

    else:
        return html_code


def crop_html_content(temp, original_html_file_path, copy_html_file_path):
    if os.path.exists(copy_html_file_path):
        with open(copy_html_file_path) as org:  # ! the copy already exists
            html_content = org.read()
            html_content = check_if_script_tag_in(html_content)
            return temp.replace(LESSON_CONTENT, html_content)

    with open(original_html_file_path) as org:
        html_content = org.read()
        #! make a copy of the original html file
        with open(copy_html_file_path, 'w') as copy:
            copy.write(html_content)

        html_content = check_if_script_tag_in(html_content)

        return temp.replace(LESSON_CONTENT, html_content)

# ?==============================================================
# ?==============================================================


def first_replace(folder_path, item_path, file_indx, is_html=False):
    temp = None
    item_name = os.path.splitext(item_path)[0]
    with open(os.path.join(SCRIPT_PATH, 'video_template.html')) as file:
        temp = file.read()\
            .replace(FOLDER_NAME_PLACEHOLDER, os.path.basename(folder_path))\
            .replace(ITEM_NAME_PLACEHOLDER, item_name)\
            .replace(ITEM_INDEX, str(file_indx+1))  # beacuse in html counting starts from 1

        # because we will replace "pylr"  with the html file content
        # also we will make a copy of the original html file
        if is_html:
            original_html_file_path = os.path.join(folder_path, item_path)
            copy_html_file_path = os.path.join(
                folder_path, item_name + '_original.html')

            return crop_html_content(temp, original_html_file_path, copy_html_file_path)

        temp = temp.replace(LESSON_CONTENT, CONTENT_VIDEO)\
            .replace(ITEM_PATH_PLACEHOLDER, item_path)

    return temp


def select_wallpaper_from(folder):
    image = None
    valid_images_exts = [".jpg", ".gif", ".png", ".tga", "jpeg"]

    for file in sorted(os.listdir(folder)):
        # if this is not a file

        ext = os.path.splitext(file)[1]
        if ext.lower() in valid_images_exts:
            image = file

    return image


def create_index_file(temp_path, folder, items_code, is_the_course_index=False):
    with open(temp_path) as file:
        html_temp = file.read()
        html_temp = html_temp.replace(
            FOLDER_NAME_PLACEHOLDER, os.path.basename(folder))

        with open(os.path.join(folder, 'index.html'), 'w') as index:
            html_temp = html_temp.replace(
                SIDEBAR_ITEMS_PLACEHOLDER, items_code)

            #! we need to select the wallpaper
            if is_the_course_index:
                image = select_wallpaper_from(folder)
                if image != None:
                    html_temp = html_temp.replace(WALPAPER_IMAGE, image)
            index.write(html_temp)


def create_videos_html_files():
    global FOLDER_TO_FILES, LIST_FOLDERS

    # first dict
    for folder_indx, folder_path in enumerate(LIST_FOLDERS):
        print(folder_path)
        print(LINE_SEP)
        # second dict
        folder = FOLDER_TO_FILES[folder_path]
        list_files = list(folder.keys())
        for file_indx, file in enumerate(list_files):
            temp = None

            # this is html file so remove "plyr"
            if file.endswith('.html'):
                temp = first_replace(
                    folder_path, file, file_indx, is_html=True)

            # this is video
            else:
                temp = first_replace(folder_path, file, file_indx)
                subs = folder[file]
                temp = subs_code(temp, subs)

            temp = next_prev_items_code(
                temp, folder_indx, file_indx, list_files)

            items_code = sidebar_items_code(list_files)
            temp = temp.replace(SIDEBAR_ITEMS_PLACEHOLDER, items_code)

            #! this is the last lesson in the unit so we need to return the items code
            #! so we can create the "index.html" file for the unit folder
            if file_indx == len(list_files) - 1:
                create_index_file(
                    os.path.join(SCRIPT_PATH, 'unit_template.html'),
                    folder_path, items_code)

            name_html_file = os.path.splitext(file)[0] + '.html'
            video_html_file = os.path.join(folder_path, name_html_file)
            print(video_html_file)
            with open(video_html_file, 'w') as html:
                html.write(temp)


def extract_video_and_subs(root, files):
    videos, subs, htmls = [], [], []

    for f in files:
        name, ext = os.path.splitext(f)
        if ext == '.mp4':  # a video
            videos.append(f)
        elif ext == '.vtt':  # vtt a sub
            subs.append(f)

        elif ext == '.srt':  # a srt sub
            # ? VERY IMPORTANT https://github.com/sampotts/plyr/issues/355
            # HTML5 specification does not support subtitle format other than webvtt,
            # so you need a webvtt format subtitle for the src.
            # so we create will convert the srt subtuile to vtt subtitle
            # if the "vtt" subtitle file did not already exists

            vtt_equivelant = name + '.vtt'

            if vtt_equivelant in subs:  # the a vtt file already exists
                continue
            else:
                srt_full_path = os.path.join(root, f)
                craete_vtt_from(srt_full_path)
                subs.append(vtt_equivelant)

        elif ext == '.html' and not f.endswith('_original.html') and f != 'index.html':
            #! some concepts in the lsseon are html files
            #! also skip copies of the original files see method crop_html_content()
            htmls.append(f)

    #! add html lesson to the videos to form the full unit lessons
    for h in htmls:
        first_two_words = ' '.join(h[:-4].split()[1:])
        if any([' '.join(v[:-3].split()[1:]) == first_two_words for v in videos]):
            continue
        videos.append(h)

    # sort the videos so the result dict keys are sorted also and we can
    # sue them at the current order to fill the HTML file
    videos.sort(key=lambda v: int(re.findall(r'\d+', v)[0]))

    #! there's no html or videos in this folder
    if videos == []:
        return None

    result = {}
    for v in videos:
        num = re.findall(r'\d+', v)[0]
        result[v] = [s for s in subs if re.findall(r'\d+', s)[0] == num]
        #  also sort the subs in place
        #  because the first one will be the default subtitle
        result[v].sort()

    return result


def copy_assets_folder():
    global COURSE_FOLDER

    dest_folder = os.path.join(COURSE_FOLDER, 'assets')
    try:
        # if the folder already exists this will raise an error
        os.mkdir(dest_folder)
    except:
        pass

    copy_tree(os.path.join(SCRIPT_PATH, 'assets'), dest_folder)


def craete_vtt_from(srt_file):
    try:
        vtt = webvtt.from_srt(srt_file)
        path_vtt_file = os.path.splitext(srt_file)[0] + '.vtt'
        vtt.save(path_vtt_file)

    #! The file does not have a valid format.
    except:
        return


for root, folders, files in os.walk(COURSE_FOLDER):
    if root == COURSE_FOLDER:
        copy_assets_folder()
        continue

    # ? VERY IMPORTAT
    #! choose only folders that starts with a number
    #! i.e. the folders downloaded from udemy not any other custom folders
    #! made by the user
    if os.path.basename(root)[0].isdigit():
        files = extract_video_and_subs(root, files)

        #! there's no html or videos in this folder
        if files == None:
            print()
            print(f'🤫 EMPTY FOLDER 🤫 => {root}')
            print(LINE_SEP)
            print()
            continue

        else:
            FOLDER_TO_FILES[root] = files


# pprint(FOLDER_TO_FILES)
# sys.exit()
LIST_FOLDERS = list(FOLDER_TO_FILES.keys())
LIST_FOLDERS.sort(key=lambda v: int(re.findall(r'\d+', v)[0]))

create_videos_html_files()

# ?==========================================================
#! create course "index.html" file
create_index_file(
    os.path.join(SCRIPT_PATH, 'course_template.html'),
    COURSE_FOLDER,
    sidebar_items_code(LIST_FOLDERS, True),
    is_the_course_index=True)
# ?==========================================================
