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
    download the whole series at onc by using IDM Descktop Or ADM android app.

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


LINE_SEP = '#' * 70
BASE_PATH = ""
BASE_LINK = 'https://podcasts.google.com'


def make_download_folder(folder_title):

    # # Getting the title from the website
    # title = soup.select('.movie_title h1')[0].getText()

    download_path = os.path.join(BASE_PATH, folder_title)
    os.makedirs(download_path, exist_ok=True)

    # Uncomment the line below to download cover image
    # cover_img(soup)

    print('download folder is ready.'.title())
    print(LINE_SEP)
    return download_path


def download_this_podcast(pocast_link):
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

        print('\tEpisode Title: ' + episode.find('title').text)  # Episode Title
        print('\tdirect link: '.title() + direct_link)
        print(LINE_SEP)
    txt.close()


def pick_download_folder():
    """
    This method launch a folder picker to choose
    the root download folder 
    """
    where_to = ''
    while not where_to:
        # Pick download folder
        print('\nplease choose where to put download folder.'.upper())
        print(LINE_SEP)
        Tk().withdraw()  # to hide the small tk window
        where_to = filedialog.askdirectory()  # folder picker

    return where_to


def check_link_and_download():
    global BASE_PATH
    pocast_links = []

    # Make the user enter as many pocast_links as he wants
    pocast_link = input(
        'Please, enter the podcast url:').strip()
    while pocast_link != '0':
        # empty the pocast_link before entering a new one
        # pocast_link = ''

        while BASE_LINK not in pocast_link:
            if pocast_link == '0':
                sys.exit()
            pocast_link = input(
                'Please, enter a valid podcast url:').strip()

        if pocast_link not in pocast_links:
            pocast_links.append(pocast_link)
        else:
            print('podcast already included in the download list!'.title())

        print('\n(%d) Podcasts To Download' % len(pocast_links))
        print('-' * 40)

        pocast_link = input(
            'Download another podcast url or enter 0 to begin: ').strip()

    print(LINE_SEP)

    if not pocast_links:  # The Download List is Empty
        print('no pocast_links to download'.title())
        sys.exit()

    # download folder picker
    BASE_PATH = pick_download_folder()

    print('\nConnecting...\n' + LINE_SEP)

    downloadThreads = []
    for link in pocast_links:
        thread = threading.Thread(target=download_this_podcast,
                                  args=[link])
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
