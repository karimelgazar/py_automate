﻿"""
This Script auto share a specific post 
to all groups filled in a txt file
"""
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys

BASE_LINK = 'https://www.facebook.com/karimCodes/posts'
BASE_LINK2 = 'https://www.facebook.com/108780843826246/posts'
post_link = input('Please Input The Post Link OR ID: ')


while True:
    if post_link.isdigit() and post_link != '108780843826246':  # ? the post ID was given
        post_link = '{}/{}'.format(BASE_LINK, post_link)
        break

    elif BASE_LINK in post_link or BASE_LINK2 in post_link:
        break

    else:
        post_link = input('Please Input A Valid Post Link: ')


# ** This is SO IMPORTANT Because it enables you to
# ** be logged in coursera automatically so that they don't
# ** know you are a bot other wise they will block you
options = webdriver.ChromeOptions()

# ? This will load the cookies and passwords from
# ? the orignal Chrome browser
options.add_argument(
    #    "--user-data-dir=\"/home/km/.config/google-chrome/Profile\ 1\"")
    "--user-data-dir=/home/km/karim/Important/automation_profile")
# ? This will reduse the amount of lines that
# ? Selenium prints to the terminal
options.add_argument("--start-maximized")
options.add_argument('--log-level=3')

# open the browser
browser = webdriver.Chrome(
    ChromeDriverManager().install(),
    options=options)
browser.get(post_link)


time.sleep(2)
# input_fields, buttons = None, None
groups = open(
    "/home/km/karim/py_automate/Facebook_Auto_Group_Posting/groups_names.txt",
    'r',
    encoding='UTF-8')

shown = False

for group_name in groups.readlines():
    if not group_name:
        continue

    group_name = group_name.strip()

    while (True):
        try:
            # STEP #1 Press Main Share Button
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Share"))).click()
            break
        except:
            time.sleep(1)
            continue

    # STEP #2 Press share in a group button
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Share in a group"))).click()
        
    # wait for the pop up window so you can input the group name
    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Share in a group")))

    #time.sleep(2)
    input_fields = browser.find_elements_by_tag_name('input')

   # STEP #3 press the CheckBox include_original_post if exists
    try:
        ActionChains(browser)\
            .move_to_element(input_fields[-1])\
            .click(input_fields[-1])\
            .perform()
    except:
        print('\n\ninclude_original_post was not found.\n'.title())

    # STEP #4 Write Group Name Then Share
    '''fixed an error: 
        The error happened when double click 
        the group name input field 
        so I make it a single click
    '''
    # input_fields[-2] = browser.find_element_by_link_text("Group name")
    # time.sleep(2)
    ActionChains(browser)\
        .move_to_element(input_fields[-2])\
        .click(input_fields[-2])\
        .perform()
    # .click(input_fields[-2])\
    #   .click(input_fields[-2])\

    if 'الانترنت' in group_name:
        group_name = 'الانترنت'

    input_fields[-2].send_keys(group_name[0])
    time.sleep(1)
    input_fields[-2].send_keys(group_name[1:])

    if not shown and group_name == 'تعلم البرمجة من الألف الى الياء':
        shown = True
        input_fields[-2].send_keys([Keys.DOWN,
                                    Keys.ENTER])

    elif shown and group_name == 'تعلم البرمجة من الألف الى الياء':
        input_fields[-2].send_keys([Keys.DOWN,
                                    Keys.DOWN,
                                    Keys.ENTER])

    else:
        input_fields[-2].send_keys([Keys.DOWN,
                                    Keys.ENTER])

    # post_button
    buttons = browser.find_elements_by_tag_name('button')
    buttons[-1].click()
    print(group_name.ljust(85) + '|DONE|' + '\n-----------------')
    time.sleep(4)  # wait sometime until the next share


browser.close()
sys.exit()
