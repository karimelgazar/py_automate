"""
Description:

    This Script Takes a link for the whole Series or a single season
    at Egybest Website from clipboard or as a terminal argument
    or user input if the user forgot.

    Then creates a root folder for the whole series(if the whole series link was given)
    and for each season the script creates an inner folder
    and name it with the season name and also downloads the cover image for
    this season.

    After that loops throw all the season episodes in the link
    and extract the direct link for every episode then saves every
    new direct link to a file (ADM.txt) so that you can
    download the whole series at onc by using IDM Descktop Or ADM android app.

"""

from tkinter import Tk, filedialog
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import webbrowser
import re
from bs4 import BeautifulSoup, NavigableString
import threading
import time
import os
import sys
import requests
import pyperclip

LINE_SEP = '#' * 70
BASE_PATH = ""
BASE_LINK = 'egy.best'

options = webdriver.ChromeOptions()
# ? This will reduse the amount of lines that
# ? Selenium prints to the terminal
options.add_argument('--log-level=3')

browser = None


def download_cover_img(link):
    print('downloading the image'.title())
    req = requests.get(link)
    req.raise_for_status()

    imageFile = open(os.path.basename(link), 'wb')

    for chunk in req.iter_content(100000):
        imageFile.write(chunk)

    imageFile.close()
    print('\nimage download finished   '.title())
    print(LINE_SEP)


def cover_img(soup):
    img_link = soup.select('.movie_img a img')[0].get('src')
    # if the image is already downloaded then
    # don't download again
    if not os.path.exists(os.path.basename(img_link)):
        threading.Thread(target=download_cover_img, args=[img_link]).start()
    else:
        print('the cover image is ready   '.title())


def make_download_folder(soup, folder_title):

    # # Getting the title from the website
    # title = soup.select('.movie_title h1')[0].getText()

    download_path = os.path.join(BASE_PATH, folder_title)
    os.makedirs(download_path, exist_ok=True)

    # Uncomment the line below to download cover image
    # cover_img(soup)

    print('download folder is ready   '.title())
    print(LINE_SEP)
    return download_path


def extract_direct_link(episode_link, browser, quality_num=2):
    print('\n\topening episode link: '.title(), episode_link)

    browser.get(episode_link)

    # The download buttons in the episode link
    # and clicking the button with the passed quality_number
    download_buttons_selector = 'a.btn.g.dl.nop._open_window'
    download_buttons = browser.find_elements_by_css_selector(
        download_buttons_selector)
    download_buttons[quality_num].click()

    # Switching to the new opened tab
    # from which we will download the episode
    browser.switch_to.window(browser.window_handles[-1])
    direct_link = browser.find_element_by_class_name(
        "bigbutton").get_attribute("href")

    if direct_link == None:
        # If there is no link with the download button
        # we need to click it to excute JS script
        browser.find_element_by_class_name("bigbutton").click()

        # If an ads tab was opened we close it
        if len(browser.window_handles) > 2:
            browser.switch_to.window(browser.window_handles[-1])
            browser.close()

        # Switch back to the download page
        browser.switch_to.window(browser.window_handles[-1])
        time.sleep(2)  # So the direct link can be loaded
        direct_link = browser.find_element_by_class_name(
            "bigbutton").get_attribute("href")

        # Close the download page and then
        # return to the episode original page
        browser.close()
        browser.switch_to.window(browser.window_handles[-1])

    print('\tDirect Download Link: ' + str(direct_link))
    print('\tStatus: Done.')
    print(LINE_SEP)
    return direct_link


def get_folder_title_from(link):
    # removing the last backslash if exists
    if link.endswith('/'):
        link = link[:-1]

    rex = re.compile(r'[\w-]+$')
    folder_title = rex.findall(link)[0]

    req = requests.get(link)
    req.raise_for_status()
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup, folder_title


def download_this_season(season_link, quality):
    print(season_link)
    print(LINE_SEP)

    soup, folder_title = get_folder_title_from(season_link)
    season_path = make_download_folder(soup, folder_title)

    # episodes_links = []
    browser = webdriver.Chrome(
        executable_path="E:\Progammes\chromedriver_win32\chromedriver.exe", chrome_options=options)

    # The .txt file must be named ADM
    # so you can download from it using Adm app
    txt = open(os.path.join(season_path, 'ADM.txt'), 'w')

    if 'movie' in season_link:
        # If the link was for a movie
        # just download this movie only
        txt.write(extract_direct_link(
            season_link, browser, quality) + '\n')
    else:
        raw_links = soup.select('.movies_small')[0]  # episodes links
        for episode in raw_links:
            if not isinstance(episode, NavigableString):
                txt.write(extract_direct_link(
                    episode.get('href'), browser, quality) + '\n')

    txt.close()
    browser.quit()


def choose_video_quality():
    print('Please, Enter the Number of your prefered Qaulity.')
    print(LINE_SEP)
    print('Full HD 1080p >> Enter Number 0')
    print('HD 720p       >> Enter Number 1')
    print('SD 480p       >> Enter Number 2')
    print('SD 360p       >> Enter Number 3')

    dic = {0: 'Full HD 1080p', 1: 'HD 720p',
           2: 'SD 480p', 3: 'SD 360p'}
    num = -1
    while num < 0 or num > 3:
        try:
            print('\nPlease, Choose a number between 0 to 3: ')
            num = int(input('Your Choosen Quality Number: '))
            print('\nOK I\'ll download it at: %s.' % dic[num])
        except:
            continue
    print(LINE_SEP)
    return num


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
    link = input('Please Enter the series link: '.title())

    # if len(sys.argv) > 1:
    #     link = sys.argv[1]
    #     # folder_title = sys.argv[2]

    if link == '0':
        sys.exit()

    print(LINE_SEP)
    # Getting the link as a terminal arguments
    while BASE_LINK not in link:
        link = input(
            'I see you forgot to enter the Series link.\nPlease, enter it:').strip()
        print(LINE_SEP)
    print()
    # the link should not end with
    # strange weird text like >> ?ref=tv-p1
    # because we want to  exrtact the folder name
    # from the link so we look for
    # the last occurance of backslash
    # and make the new text from
    # the beginning until last occurence
    link = link[:link.rfind('/')]

    quality = choose_video_quality()

    print('\nConnecting...\n' + '#'*50 + '\n')

    if 'series' in link:
        # Making the series root Path
        # and Getting the folder title from the link adress
        print(link)
        print(LINE_SEP)

        soup, folder_title = get_folder_title_from(link)
        series_path = make_download_folder(soup, folder_title)

        # The links for the whole sereies seasons
        a_tags = soup.select('.contents.movies_small')[0]

        # Pick where to put the download folder
        BASE_PATH = pick_download_folder()

        downloadThreads = []
        for a in a_tags:
            if not isinstance(a, NavigableString):
                # NavigableString Is an invalid tag in html so
                # We need to avoid it by checking if our tag object
                # is an instance of this class
                thread = threading.Thread(target=download_this_season,
                                          args=[a.get('href'), quality])
                thread.start()
                downloadThreads.append(thread)

        for thread in downloadThreads:
            # Make the main thred wait until
            # all the threads finish working
            thread.join()

        return

    download_this_season(link, quality)


########################################################
# THE SCRIPT STARTS EXCUTING FROM HERE
########################################################
print(LINE_SEP)
print('\t\t\tHow To Use\n\t\t', '-' * 25)
print('Enter the Series link to download'.title(),
      'Enter 0 to exit.'.title(), sep='\n')
print(LINE_SEP)

check_link_and_download()
webbrowser.open(BASE_PATH)

sys.exit()
