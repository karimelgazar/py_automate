"""
Description:

    This Script Takes a movie or Series link at Akoam Website
    as a user input if the user forgot and then creates a folder
    with the series name and also downloads the cover image
    then loops throw all the series episodes in the link
    and extract the direct link for every episode then saves every 
    new direct link to a file .txt so that you can
    download the whole series at onc by using IDM.
"""

from tkinter import Tk, filedialog
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import selenium.common.exceptions as sel_exceptions
import webbrowser
import re
from bs4 import BeautifulSoup
import threading
import time
import os
import sys
import requests
import pyperclip

LINE_SEP = '#' * 50
BASE_PATH = ""
BASE_LINK = 'akoam.net'
# TEST_LINK = 'https://we.akoam.net/162829/%D9%85%D8%B3%D9%84%D8%B3%D9%84-Dororo-%D8%A7%D9%84%D9%85%D9%88%D8%B3%D9%85-%D8%A7%D9%84%D8%A7%D9%88%D9%84-%D9%85%D8%AA%D8%B1%D8%AC%D9%85'

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
    print('\nimage download finished ✅ ✅ ✅'.title())
    print(LINE_SEP)


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


def make_download_folder(soup):
    global BASE_PATH
    # Getting the title from the website
    title = soup.select('.sub_title h1')[0].getText()
    rex = re.compile(r'[\w ]+')
    folder_title = rex.search(title).group()

    BASE_PATH = pick_download_folder()

    download_path = os.path.join(BASE_PATH, folder_title)
    os.makedirs(download_path, exist_ok=True)
    os.chdir(download_path)

    img_link = soup.select('.main_img')[0].get('src')
    # if the image is already downloaded then
    # don't download again
    if not os.path.exists(os.path.basename(img_link)):
        threading.Thread(target=download_cover_img, args=[img_link]).start()
    else:
        print('the cover image is ready ✅ ✅ ✅'.title())
    print('download folder is ready ✅ ✅ ✅'.title())
    print(LINE_SEP)


def prepare_links():
    global browser, options
    link = input('Please Enter the series or movie link: '.title())

    # A list of two lists:
    # the the list at index [0] contains episodes names
    # the the list at index [1] contains episodes ads-links
    titles_ads_link = [[], []]

    folder_title = ''

    if link == '0':
        sys.exit()

    print(LINE_SEP)
    # Getting the link as a terminal arguments
    while BASE_LINK not in link:
        link = input(
            'I see you forgot to enter the Series link.\nPlease, enter it:').strip()
        print(LINE_SEP)
    print()

    print('\nConnecting...\n' + '#'*50)

    req = requests.get(link)
    req.raise_for_status()
    soup = BeautifulSoup(req.text, 'html.parser')

    make_download_folder(soup)

    all_epi_titles = soup.select('.sub_file_title')
    all_epi_links = soup.select('.akoam-buttons-group a')

    # the increment in the for loop is 2
    # beacause the download button and watch online button
    # have the same link and download button link is at
    # even indexes in all_epi_links list
    for i in range(0, len(all_epi_links), 2):
        titles_ads_link[0].append(all_epi_titles[i // 2].getText())
        titles_ads_link[1].append(all_epi_links[i].get('href'))

    browser = webdriver.Chrome(
        executable_path="E:\Progammes\chromedriver_win32\chromedriver.exe", chrome_options=options)

    return titles_ads_link


def extract_direct_link(ads_link):
    global browser

    print('\topening ads-link url...'.title())
    browser.get(ads_link)

    download_page_link = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Click Here"))).get_attribute("href")
    print('\tDownload Page Link: ' + download_page_link)

    browser.get(download_page_link)
    direct_link = WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "download_button"))).get_attribute("href")
    print('\tDirect Download Link: ' + str(direct_link))
    print('\tStatus: Done. ✅ ✅ ✅')

    return direct_link


########################################################
# THE SCRIPT STARTS EXCUTING FROM HERE
########################################################
print(LINE_SEP)
print('\t\t\tHow To Use\n\t\t', '-' * 25)
print('Enter the Series link to download'.title(),
      'Enter 0 to exit.'.title(), sep='\n')
print(LINE_SEP)

all = prepare_links()
series_direct_links = open('series_direct_links.txt', 'w')
i = 0
for title, ads_link in zip(all[0], all[1]):
    print('Episode:\n\tTitle: ' + title)
    print('\tAds-Link: ' + ads_link)
    try:
        series_direct_links.write(extract_direct_link(ads_link) + '\n')
        print('\ttxt file: direct link saved. ✅ ✅ ✅'.title())
        i += 1
    except Exception as error:
        print('%' * 50)
        print('\nSomeThing Went Wrong! ❌ ❌ ❌\n')
        print('With Episode:\n\t%s\n\t%s' % (title, ads_link))
        print('\nSo I Skipped It And Moved To The Next Episode\n\n')
        print('The error message:\n%s' % error)
        continue

    print(LINE_SEP)

browser.quit()
series_direct_links.close()

webbrowser.open(BASE_LINK)
sys.exit()
