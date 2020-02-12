"""
this program allows you to extract the direct links of anime episodes 
from ww1.animeiat.co website and save these links to ADM.txt
in the any place you want 

further more it allows to download more than one series at the same time
also allows you to download with IDM
"""

from tkinter import Tk, filedialog
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
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
BASE_LINK = ".animeiat.co/tvshows/"

options = webdriver.ChromeOptions()
# ? This will reduse the amount of lines that
# ? Selenium prints to the terminal
options.add_argument('--log-level=3')


def get_folder_title_from(link):
    # removing the last backslash if exists
    if link.endswith('/'):
        link = link[:-1]

    req = requests.get(link)
    req.raise_for_status()
    soup = BeautifulSoup(req.text, 'html.parser')

    year = soup.select('td > a')[1].text + '_'
    rex = re.compile(r'[\w-]+$')
    folder_title = year + rex.findall(link)[0]

    return soup, folder_title


def make_download_folder(folder_title):

    # Getting the title from the website
    # title = soup.select('.movie_title h1')[0].getText()

    #! remove special charcter that windows doesn't accept as a folder name
    folder_title = re.sub(r"[-*:/<>?\|]", "_", folder_title)

    download_path = os.path.join(BASE_PATH, folder_title)
    os.makedirs(download_path, exist_ok=True)

    # Uncomment the line below to download cover image
    # cover_img(soup)

    print('output folder is ready.'.title())
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


def extract_direct_link(episode_link, browser, quality_num=1):
    print(LINE_SEP)
    print('\tepisode link:'.title(), episode_link)
    browser.get(episode_link)

    #########################################
    #! before going to the download process
    #########################################

    # click the watch button to go to a pop-up page
    # the pop-up page is either download or ads page
    watch_button_selector = '#watch-btn > i'
    watch_button = browser.find_element_by_css_selector(watch_button_selector)
    watch_button.click()

    # Switching to the new opened tab
    # from which we will download the episode
    browser.switch_to.window(browser.window_handles[-1])

    first_download_button_selector = 'body > div > div.download-servers.text-center > a'
    try:
        first_download_button = browser.find_element_by_css_selector(
            first_download_button_selector)

    # ? If there is no download button then we are in ads page
    except:
        # if first_download_button == None:
        # If an ads tab was opened we close it

        browser.close()
        browser.switch_to.window(browser.window_handles[-1])

        # while len(browser.window_handles) > 1:
        #     browser.close()
        #     browser.switch_to.window(browser.window_handles[-1])

        # Switch back to the episode page
        # browser.switch_to.window(browser.window_handles[0])
        # watch_button = browser.find_element_by_css_selector(
        #     watch_button_selector)
        # watch_button.click()

    first_download_button = browser.find_element_by_css_selector(
        first_download_button_selector)

    ##################################
    #! the download process
    ##################################

    # ? the download button text
    db_label = first_download_button.text

    if db_label == 'Animeiat':  # ! it was a direct link
        # Close the download page and then
        # return to the episode original page
        direct_link = first_download_button.get_attribute('href')
        print('\tDirect Download Link: ' + str(direct_link))
        print(LINE_SEP, '\n')

        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        return direct_link

    # go to the download page
    # '/v/' display the video and there is no download button
    # so change it to '/f/' to display the download button
    download_page_link = first_download_button.get_attribute('href').replace(
        '/v/', '/f/')
    browser.get(download_page_link)

    # the big download button
    browser.find_element_by_css_selector(
        'button#download.button.is-primary').click()

    # waiting for the video quality download buttons to appear
    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "a.button.is-medium.is-success.clickdownload")))

    d_buttons = browser.find_elements_by_css_selector(
        "a.button.is-medium.is-success.clickdownload")

    direct_link = d_buttons[quality_num].get_attribute("href")
    print('\tDirect Download Link: ' + str(direct_link))
    print('\tStatus: Done.')
    print(LINE_SEP, '\n')

    # Close the download page and then
    # return to the episode original page
    browser.close()
    browser.switch_to.window(browser.window_handles[0])

    return direct_link


def download_this_anime(anime_link, quality_num, use_idm):

    print(anime_link)
    print(LINE_SEP)

    soup, folder_title = get_folder_title_from(anime_link)
    anime_path = make_download_folder(folder_title)

    # episodes_links = []
    browser = webdriver.Chrome(
        executable_path="E:\Progammes\chromedriver_win32\chromedriver.exe",
        chrome_options=options)

    # The .txt file must be named ADM
    # so you can download from it using Adm app
    txt = open(os.path.join(anime_path, 'ADM.txt'), 'w')

    #! episodes links
    raw_links = soup.select(
        '#main > div > section:nth-child(2) > div > article > a')

    for episode in raw_links:
        if not isinstance(episode, NavigableString):
            direct_link = extract_direct_link(episode.get('href'), browser,
                                              quality_num)
            txt.write(direct_link + '\n')

            if use_idm.lower() == 'y':
                # last episode to download
                if raw_links.index(episode) == len(raw_links) - 1:
                    download_with_IDM(direct_link, anime_path,
                                      os.path.basename(direct_link), True)
                else:
                    download_with_IDM(direct_link, anime_path,
                                      os.path.basename(direct_link))

    txt.close()
    browser.quit()


def pick_output_folder():
    """
    This method launch a folder picker to choose
    the root download folder 
    """
    where_to = ''
    while not where_to:
        # Pick download folder
        print('\nplease choose where to put the output folder.'.title())
        print(LINE_SEP)
        Tk().withdraw()  # to hide the small tk window
        where_to = filedialog.askdirectory()  # folder picker

    return where_to


def choose_video_quality():
    print('Please, Enter the Number of your prefered Qaulity.')
    print(LINE_SEP)
    print('SD 480p  >>  Enter Number 0')
    print('HD 720p  >>  Enter Number 1')

    dic = {0: 'SD 480p', 1: 'HD 720p'}

    num = -1
    while num < 0 or num > 3:
        try:
            print('\nPlease, input number 0 or 1: ')
            num = int(input('Your Choosen Quality Number: '))
            print('\nOK I\'ll download it at: %s.' % dic[num])
        except:
            continue
    print(LINE_SEP)
    return num


def check_link_and_download():
    global BASE_PATH
    anime_links = []

    #! Make the user enter as many anime_links as he wants
    anime_link = input('Please, enter the anime url:').strip()

    while anime_link != '0':

        while BASE_LINK not in anime_link:
            if anime_link == '0':
                if len(anime_links) == 0:
                    sys.exit()
                else:
                    break  # the inner loop
            anime_link = input('Please, enter a valid anime url:').strip()

        if anime_link == '0':
            break  # the outer loop
        if anime_link not in anime_links:
            anime_links.append(anime_link)
        else:
            print('anime already included in the download list!'.title())

        print('\n(%d) Animes To Download' % len(anime_links))
        print('-' * 40)

        anime_link = input(
            'Enter another anime url to download or enter 0 to begin: ').strip(
            )

    print(LINE_SEP)

    if not anime_links:  # The Download List is Empty
        print('no anime links to download'.title())
        sys.exit()

    #! choose the quality
    quality_num = choose_video_quality()

    #! output folder picker
    BASE_PATH = pick_output_folder()

    #! download with IDM or not
    use_idm = 'k'
    while use_idm.lower() != 'y' and use_idm.lower() != 'n':
        use_idm = input("download with IDM after completion[y/n]: ").title()
        print(LINE_SEP)

    print('\nConnecting...\n' + '#' * 50 + '\n')

    downloadThreads = []
    for link in anime_links:
        thread = threading.Thread(target=download_this_anime,
                                  args=[link, quality_num, use_idm])
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
      'Enter 0 to begin or exit if no links were entered.'.title(),
      sep='\n')
print(LINE_SEP)

check_link_and_download()
webbrowser.open(BASE_PATH)

sys.exit()
