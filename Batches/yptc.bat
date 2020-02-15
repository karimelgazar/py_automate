@python "E:/karim/Py_Automate/youtube_playlists_time_counter.py"
IF ERRORLEVEL 1 PAUSE && EXIT

"""
Description:

    This Script Takes a link for a group of playlists or a single playlist
    then calculate the total time for the videos in it or them.

    After that the script will extract a txt file with information about
    this playlist.

    The file name will be the same as the youtube channel name.
"""
from tkinter import filedialog, Tk
import requests
from bs4 import BeautifulSoup
import sys
import os
import webbrowser
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

LINE_SEP = '-' * 70 + '\n'
BASE_LINK = 'https://www.youtube.com'
PLAYLIST_BASE_LINK = 'https://www.youtube.com/playlist?'


def extract_time(time_texts):
    """takes a list of string times 
        and return the total time 
        with a leading zero like >> 01:00:01

    Arguments:
        time_texts {[a list of strings]} 

    Returns:
        [string] -- [return the total time of hours, minutes and seconds
        with a leading ZERO using the method zfill()]
    """
    tot_hours, tot_minutes, tot_seconds = (0, 0, 0)
    all_times = [time.split(':') for time in time_texts]

    for time in all_times:
        """Use [-1] to the last element whatever the list length is"""
        tot_seconds += int(time[-1])

        """Use [-2] to get the element before the last element whatever the list length is"""
        tot_minutes += int(time[-2])

        if len(time) > 2:
            tot_hours += int(time[0])

    sec = tot_seconds % 60
    tot_minutes += (tot_seconds - sec) // 60
    minu = tot_minutes % 60
    h = tot_hours + (tot_minutes - minu) // 60
    return '%s Hours, %s Minutes, %s Seconds' % (str(h).zfill(2), str(minu).zfill(2), str(sec).zfill(2))


def info_of_this_playlist(playlist_link, html, txt_file=None):
    """Extract information for a single playlist"""
    txt_was_None = False
    file_name = None

    soup = BeautifulSoup(html, 'html.parser')

    playlist_title = soup.select(
        '#title > yt-formatted-string > a')[0].text

    total_videos = soup.select(
        '#stats > yt-formatted-string:nth-child(1)')[0].text
    videos_num = int(total_videos.split()[0])

    """
    Take the number of times for only the total number
    of videos in the playlist because in some playlists 
    the CSS selector might lead you to a video in another 
    playlist or even a another channel channel.   
    
    """
    times = [tag.text.strip() for tag in soup.select(
        '.ytd-thumbnail-overlay-time-status-renderer')[:videos_num]]

    total_time = extract_time(times)

    print(playlist_title, total_time, '-'*50, sep='\n')

    if not txt_file:
        """
        create a txt file because the txt_file is None
        so the original link is for a single playlist  
        """
        txt_was_None = True
        file_name = soup.select('#text > a')[0].text + '.txt'
        txt_file = open(file_name, 'w', encoding='UTF-8')

    txt_file.write('\t\t| ' + playlist_title + ' |\n\n' +
                   'playlist link: '.title() + playlist_link + '\n'
                   'total videos number: '.title() + total_videos + '\n' +
                   'total time: '.title() + total_time + '\n' + LINE_SEP)

    if txt_was_None:
        txt_file.close()
        """ Open the txt file after finishing """
        webbrowser.open(file_name)


def info_of_all_playlists(link):
    """Extract information for a link of a group of playlists"""
    bro = webdriver.Chrome()
    bro.get(link)

    soup = BeautifulSoup(bro.page_source, 'html.parser')

    channel_title = soup.select('#text')[2].text

    """Playlists links from the link """
    links = [BASE_LINK + playlist.get('href')
             for playlist in soup.select('#view-more > a')]

    """naming the file as the same name as the channel"""
    file_name = channel_title + '.txt'
    txt_file = open(file_name, 'w', encoding='UTF-8')

    for playlist_link in links:
        bro.get(playlist_link)

        """Wait until all the videos are loaded
        so that the total time does not become ZERO."""
        WebDriverWait(bro, 10).until(
            EC.presence_of_all_elements_located((
                By.CSS_SELECTOR,
                ".ytd-thumbnail-overlay-time-status-renderer")))
        info_of_this_playlist(playlist_link, bro.page_source, txt_file)

    bro.quit()
    txt_file.close()

    """ Open the txt file after finishing """
    webbrowser.open(file_name)


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


def check_link():
    """
    this method let the user enter a link
    then it decides weather it's a single playlist link or 
    a group of playlist and accordingly calls the appropiate method.

    and loops again if the link was invalid
    so the user can enter the correct link.
    """

    link = input('Enter the playlist or playlists link: ')
    os.chdir(pick_download_folder())  # change the working directory

    while link != '0':
        if link.startswith(PLAYLIST_BASE_LINK):
            """A link for a single list"""
            bro = webdriver.Chrome()
            bro.get(link)
            info_of_this_playlist(link, bro.page_source)
            bro.quit()
            return

        elif link.startswith(BASE_LINK) and link.endswith('/playlists'):
            """A link for a group of lists"""
            info_of_all_playlists(link)
            return

        else:
            """ invalid input """
            link = input(
                'Please,Enter 0 to exit or Enter a valid playlist link: ')


########################################################
# THE SCRIPT STARTS EXCUTING FROM HERE
########################################################
print(LINE_SEP)
print('\t\t\tHow To Use\n\t\t', '-' * 25)
print('Enter the Playlist link to Calculate Total Time.'.title(),
      'Enter 0 to exit.'.title(), sep='\n')
print(LINE_SEP)

check_link()
sys.exit()
