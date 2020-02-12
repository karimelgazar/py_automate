"""
this program extract Mega links for the anime episodes
from any one of the following websites:
    1:  https://www.arabsama.com
    2:  https://www.dotrani.net


to to able to log in to your Mega account you
need to create a [data.txt] file (with this exact name)
in the same directory of the program and in the txt file
write:
    1: YOUR EMAIL in first line of the txt file
    2: YOUR PASSWORD in  the second line of the txt file  

when you fill the txt file with your account information
you can use the program by inputing a link to any anime in the above websites
then the program will create a folder with the anime name in your account
and puts all the episodes inside it 

NOTE:
The program can handle more than one link at the same time 
"""


from bs4 import BeautifulSoup
import requests
import re
import sys
import time
import urllib
import threading
from mega import Mega

SCRIPT_BASE_PATH = sys.path[0]
BASE_LINK = "https://www.arabsama.com"
BASE_LINK_2 = "https://www.dotrani.net"
LINE_SEP = '=' * 50
PROFILE = None


def get_ids_for(anime_link):

    req = requests.get(anime_link)
    req.raise_for_status()

    # id_regx_dot = re.compile(r'mega\.nz(?:%2F%23%21)?(?:/#!)?([\w\d\-_%!]+)(?:&)?')
    # id_regx_sama = re.compile(

    id_regx = re.compile(r'(mega.nz\S+)"')
    list_of_ids = id_regx.findall(req.text)

    to_delete = []
    for i in range(len(list_of_ids)):
        # the length of correct id is 54
        # but the regex return some text shorter than that
        # so we delete it, we can't delete them directly in this loop
        # because the indcies change when we delete elements from the list
        list_of_ids[i] = list_of_ids[i].split('&')[0]

        if len(list_of_ids[i]) <= 50:
            to_delete.append(i)

    for i in to_delete:
        if i >= len(list_of_ids):
            i = -1

        del list_of_ids[i]

    return list_of_ids


def login():
    data = open(SCRIPT_BASE_PATH + '/data.txt', 'r').readlines()
    email, password = map(str.strip, data)  # remove \n
    return Mega().login(email, password)


def anime_title(anime_link):
    anime_title_regx = re.compile(r'/([\w\-]+)\.html')
    return anime_title_regx.findall(anime_link)[-1]


def add_to_mega(anime_link):
    global PROFILE

    title = anime_title(anime_link)
    print(title, LINE_SEP, sep='\n')

    PROFILE.create_folder(title)

    ids = get_ids_for(anime_link)

    time.sleep(1)  # wait for ids to finish
    for id in ids:
        # we need to decode the special character encoding in the url
        # se we use the unquote method to convert (%23) 👉👉 (#)
        url = urllib.parse.unquote("https://" + id)
        print(url)

        folder_node = PROFILE.find(title)[1]
        PROFILE.import_public_url(url, dest_node=folder_node)

    print(LINE_SEP)
    print('{} Episodes Done.'.format(len(ids)))
    print(LINE_SEP)


def enter_anime_link():
    # Make the user enter as many anime_links as he wants
    anime_links = []
    anime_link = input(
        'Please, enter the Anime url:').strip()
    while anime_link != '0':

        while BASE_LINK not in anime_link and BASE_LINK_2 not in anime_link:
            if anime_link == '0':
                if len(anime_links) == 0:
                    sys.exit()
                else:
                    break  # the inner loop
            anime_link = input(
                'Please, enter a valid Anime url:').strip()

        if anime_link == '0':
            break  # the outer loop
        if anime_link not in anime_links:
            anime_links.append(anime_link)
        else:
            print('anime already included in the download list!'.title())

        print('\n(%d) animes To Download' % len(anime_links))
        print('-' * 40)

        anime_link = input(
            'Enter another Anime url to download or enter 0 to begin: ').strip()

    print(LINE_SEP)

    if not anime_links:  # The Download List is Empty
        print('no anime_links to download'.title())
        sys.exit()

    print('\nConnecting...\n' + LINE_SEP)

    global PROFILE
    PROFILE = login()  # start logging in after all links are entered

    downloadThreads = []
    for link in anime_links:
        thread = threading.Thread(target=add_to_mega,
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
print('Enter the Anime link to add it to the download list'.title(),
      'Enter 0 to begin or to exit if no links were entered.'.title(), sep='\n')
print(LINE_SEP)


enter_anime_link()

# id_regx = re.compile(r'(mega.nz.*)\"$')
# file = 'جميع حلقات انمي Kaiji S2 مترجم - عرب ساما.html'
# list_of_ids = id_regx.findall(open(file, 'r', encoding="UTF-8").read())
# print(list_of_ids)
