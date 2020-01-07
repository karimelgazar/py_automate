"""
Description:

    This Script Takes a link for the whole Podcast from
    Chrome browser.
    (You can open the podcast in google podcast app
    then press SHARE and this will give you a link to play the podcast
    in the browser)

    After that the script loops throw all the episodes in the podcast
    and extract the direct link for every episode then saves every
    new direct link to a file (ADM.txt) so that you can
    download the whole series at once by:
    1- At the end of the program accepting the option to download with IDM Descktop
    2- ADM android app.

"""
from tkinter import filedialog, Tk
import webbrowser
import re
import threading
import time
import os
import sys
import requests
import xml.etree.ElementTree as et
from bs4 import BeautifulSoup, NavigableString
from subprocess import Popen as pop
import re


LINE_SEP = '#' * 70
BASE_PATH = ""
BASE_LINK = 'https://podcasts.google.com'


def make_download_folder(folder_title):

    # # Getting the title from the website
    # title = soup.select('.movie_title h1')[0].getText()

   #! remove special charcter that windows doesn't accept as a folder name
    folder_title = re.sub(
        r"[*:/<>?\|]", "_", folder_title)

    download_path = os.path.join(BASE_PATH, folder_title)
    os.makedirs(download_path, exist_ok=True)

    # Uncomment the line below to download cover image
    # cover_img(soup)

    print('download folder is ready.'.title())
    print(LINE_SEP)
    return download_path


def download_this_podcast(pocast_link, use_idm):
    print(pocast_link)
    print(LINE_SEP)

    req = requests.get(pocast_link)
    req.raise_for_status()

    soup = BeautifulSoup(req.text, 'html.parser')

    # Extracting the XML link
    result = soup.select(
        '#yDmH0d > c-wiz > div > div.ZfkSrd > c-wiz > div')[0]

    # The XML link will end with (") so remove it
    rex = re.compile('http\S+')
    xml_link = rex.findall(str(result))[0][:-1]

    req_xml = requests.get(xml_link)
    tree = et.fromstring(req_xml.text)

    folder_title = tree.find('channel/title').text  # Channel Title
    podcast_path = make_download_folder(folder_title)

    # The .txt file must be named ADM
    # so you can download from it using Adm app
    txt = open(os.path.join(podcast_path, 'ADM.txt'), 'w')

    episodes = tree.findall('channel/item')  # Episodes Root Path
    for episode in episodes:
        direct_link = episode.find('enclosure').get(
            'url')  # Episode Direct Link
        txt.write(direct_link + '\n')

        title = episode.find('title').text.strip() + '.mp3'
        print('\tEpisode Title: {}'.format(title))  # Episode Title
        print('\tdirect link: '.title() + direct_link)

        # download with IDM
        if use_idm.lower() == 'y':
            if (episodes.index(episode) == len(episodes) - 1):  # the last one
                download_with_IDM(direct_link, podcast_path, title, True)
            else:
                download_with_IDM(direct_link, podcast_path, title)

            print(LINE_SEP)
    txt.close()


def pick_output_folder():
    """
    This method launch a folder picker to choose
    the root download folder
    """
    where_to = ''
    while not where_to:
        # Pick download folder
        print('\nplease choose where the output folder.'.title())
        print(LINE_SEP)
        Tk().withdraw()  # to hide the small tk window
        where_to = filedialog.askdirectory()  # folder picker

    return where_to


def download_with_IDM(direct_link, directory, file_name, last=False):
    """
    download the links with idm after extracting
    you should see this link to see all the avilable
    parameter that you can pass in the terminal
    https://www.internetdownloadmanager.com/support/command_line.html


    Arguments:
        directory  -- the output directory where the links txt file
        links_txt  -- the txt file that has the direct links
    """
    change_terminal_to_utf_8 = "chcp 65001"
    IDM_DIRECTORY = "\"C:\Program Files (x86)\Internet Download Manager\IDMan.exe\""
    local_path = ' /p \"{}\"'.format(directory.replace('/', '\\').strip())
    no_questions = ' /n'
    add_to_queue = ' /a'
    start_queue = ' /s'
    download_link = ' /d \"{}\"'.format(direct_link.strip())
    file_name = re.sub(
        r"[*:/<>?\|]", "_", file_name)
    local_file_name = ' /f \"{}\"'.format(file_name.strip())

    #! the program will name arabic files as ????
    #! this is beacause windows doesn't support passing utf-8
    #! parameters in the terminal so IDM will get the name wrong as ????

    # ? change terminal code page to UTF-8 BUT DID NOT WORK EITHER
    # pop(change_terminal_to_utf_8, shell=True)

    COMMAND = IDM_DIRECTORY + download_link + \
        local_path + local_file_name + no_questions + add_to_queue

    pop(COMMAND, shell=True)  # download file

    # all files are added so start queue now because you can't start queue
    # while adding a file at the same time
    if last:
        pop(IDM_DIRECTORY + start_queue, shell=True)


def check_link_and_download():
    global BASE_PATH
    podcast_links = []

    # Make the user enter as many podcast_links as he wants
    pocast_link = input(
        'Please, enter the podcast url:').strip()
    while pocast_link != '0':

        while BASE_LINK not in pocast_link:
            if pocast_link == '0':
                if len(podcast_links) == 0:
                    sys.exit()
                else:
                    break  # the inner loop
            pocast_link = input(
                'Please, enter a valid podcast url:').strip()

        if pocast_link == '0':
            break  # the outer loop
        if pocast_link not in podcast_links:
            podcast_links.append(pocast_link)
        else:
            print('podcast already included in the download list!'.title())

        print('\n(%d) Podcasts To Download' % len(podcast_links))
        print('-' * 40)

        pocast_link = input(
            'Enter another podcast url to download or enter 0 to begin: ').strip()

    print(LINE_SEP)

    if not podcast_links:  # The Download List is Empty
        print('no podcast_links to download'.title())
        sys.exit()

    # output folder picker
    BASE_PATH = pick_output_folder()

    # download with IDM or not
    use_idm = 'k'
    while use_idm.lower() != 'y' and use_idm.lower() != 'n':
        use_idm = input("download with IDM after completion[y/n]: ").title()
        print(LINE_SEP)

    print('\nConnecting...\n' + LINE_SEP)

    downloadThreads = []
    for link in podcast_links:
        thread = threading.Thread(target=download_this_podcast,
                                  args=[link, use_idm])
        thread.start()
        downloadThreads.append(thread)

    for thread in downloadThreads:
        # Make the main thred wait until
        # all the threads finish working
        thread.join()


########################################################
# THE SCRIPT STARTS EXCUTING FROM HERE
########################################################

print(LINE_SEP)
print('\t\t\tHow To Use\n\t\t', '-' * 25)
print('Enter the Podcast link to add it to the download list'.title(),
      'Enter 0 to begin or exit if no links were entered.'.title(), sep='\n')
print(LINE_SEP)

check_link_and_download()
webbrowser.open(BASE_PATH)

sys.exit()
