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

    NEW FEATURE:
    ============
    NOW there's an option to download with IDM or not so that
    any direct linkextracted will be added to the queue in IDM
    then when all links are extracted the queue will begin.

"""

from tkinter import Tk, filedialog
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from subprocess import Popen as pop
import webbrowser
import re
from bs4 import BeautifulSoup, NavigableString
import threading
import time
import os
import sys
import requests
import pyperclip
import re

LINE_SEP = '#' * 70
BASE_PATH = ""
BASE_LINK = 'egybest'

options = webdriver.ChromeOptions()
# ? This will reduse the amount of lines that
# ? Selenium prints to the terminal
options.add_argument('--log-level=3')


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
    file_name = re.sub(r"[*:/<>?\|]", "_", file_name)
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


def click_to_reload(browser):
    tab_url = browser.current_url

    if 'egybest' not in tab_url and 'vidstream.online' not in tab_url:
        browser.close()
        browser.switch_to.window(browser.window_handles[-1])

    element_to_click = browser.find_element_by_css_selector(
        "a.bigbutton._reload")

    if element_to_click == None:
        return None

    else:
        download_page = browser.current_url
        time.sleep(2)  # So the direct link can be loaded
        element_to_click.click()
        return download_page


def extract_direct_link(episode_link, browser, quality_num=2):
    print('\n\topening episode link: '.title(), episode_link)

    browser.get(episode_link)

    # The download buttons in the episode link
    # and clicking the button with the passed quality_number
    download_buttons_selector = 'a.btn.g.dl._open_window'
    download_buttons = browser.find_elements_by_css_selector(
        download_buttons_selector)
    download_buttons[quality_num].click()

    # Switching to the new opened tab
    # from which we will download the episode
    browser.switch_to.window(browser.window_handles[-1])

    # close any page that has a url not in the urls below
    tab_url = browser.current_url
    download_page = None
    direct_link = None

    direct_link = browser.find_element_by_class_name(
        "bigbutton").get_attribute("href")

    while direct_link == None:
        # If there is no link with the download button
        # we need to click it to excute JS script
        # browser.find_element_by_class_name("bigbutton").click()

        download_page = click_to_reload(browser)

        # If an ads tab was opened we close it
        if len(browser.window_handles) > 2:
            browser.close()
            browser.switch_to.window(browser.window_handles[-1])

        if 'vidstream.online' not in browser.current_url:
            browser.get(download_page)

        # Switch back to the download page
        browser.switch_to.window(browser.window_handles[-1])
        # body > div.mainbody > div > p: nth-child(4) > a.bigbutton._reload
        time.sleep(2)  # So the direct link can be loaded
        direct_link = WebDriverWait(browser, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "bigbutton")))[0].get_attribute("href")

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


def download_this_season(season_link, quality, use_idm):
    print(season_link)
    print(LINE_SEP)

    soup, folder_title = get_folder_title_from(season_link)
    season_path = make_download_folder(soup, folder_title)

    # episodes_links = []
    browser = webdriver.Chrome(
        ChromeDriverManager().install(),
        chrome_options=options)

    # The .txt file must be named ADM
    # so you can download from it using Adm app
    txt = open(os.path.join(season_path, 'ADM.txt'), 'w')

    if 'movie' in season_link:
        # If the link was for a movie
        # just download this movie only
        direct_link = extract_direct_link(season_link, browser, quality)

        txt.write(direct_link + '\n')

        if use_idm.lower() == 'y':
            download_with_IDM(direct_link, season_path,
                              os.path.basename(direct_link), True)

    else:
        raw_links = soup.select('.movies_small')[0]  # episodes links
        for episode in raw_links:
            if not isinstance(episode, NavigableString):
                direct_link = extract_direct_link(episode.get('href'), browser,
                                                  quality)
                txt.write(direct_link + '\n')

                if use_idm.lower() == 'y':
                    # last episode to download
                    if raw_links.index(episode) == len(raw_links) - 1:
                        download_with_IDM(direct_link, season_path,
                                          os.path.basename(direct_link), True)
                    else:
                        download_with_IDM(direct_link, season_path,
                                          os.path.basename(direct_link))

    txt.close()
    browser.quit()


def choose_video_quality():
    print('Please, Enter the Number of your prefered Qaulity.')
    print(LINE_SEP)
    print('Full HD 1080p >> Enter Number 0')
    print('HD 720p       >> Enter Number 1')
    print('SD 480p       >> Enter Number 2')
    print('SD 360p       >> Enter Number 3')

    dic = {0: 'Full HD 1080p', 1: 'HD 720p', 2: 'SD 480p', 3: 'SD 360p'}
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
            'I see you forgot to enter the Series link.\nPlease, enter it:'
        ).strip()
        print(LINE_SEP)

    # Pick where to put the download folder
    BASE_PATH = pick_download_folder()

    # download with IDM or not
    use_idm = 'k'
    while use_idm.lower() != 'y' and use_idm.lower() != 'n':
        use_idm = input("download with IDM after completion[y/n]: ").title()
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

    print('\nConnecting...\n' + '#' * 50 + '\n')

    if 'series' in link:
        # Making the series root Path
        # and Getting the folder title from the link adress
        print(link)
        print(LINE_SEP)

        soup, folder_title = get_folder_title_from(link)
        series_path = make_download_folder(soup, folder_title)

        # The links for the whole sereies seasons
        a_tags = soup.select('.contents.movies_small')[0]

        downloadThreads = []
        for a in a_tags:
            if not isinstance(a, NavigableString):
                # NavigableString Is an invalid tag in html so
                # We need to avoid it by checking if our tag object
                # is an instance of this class
                thread = threading.Thread(
                    target=download_this_season,
                    args=[a.get('href'), quality, use_idm])
                thread.start()
                downloadThreads.append(thread)

        for thread in downloadThreads:
            # Make the main thred wait until
            # all the threads finish working
            thread.join()

        return

    download_this_season(link, quality, use_idm)


########################################################
# THE SCRIPT STARTS EXCUTING FROM HERE
########################################################
print(LINE_SEP)
print('\t\t\tHow To Use\n\t\t', '-' * 25)
print('Enter the Series link to download'.title(),
      'Enter 0 to exit.'.title(),
      sep='\n')
print(LINE_SEP)

check_link_and_download()
webbrowser.open(BASE_PATH)

sys.exit()
