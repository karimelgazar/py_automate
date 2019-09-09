"""
This Script auto share a specific post 
to all groups filled in a txt file
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys


BASE_LINK = 'https://www.facebook.com/karimCodes/posts/'
BASE_LINK2 = 'https://www.facebook.com/108780843826246/posts'

post_link = input('Please Input The Post Link: ')
while BASE_LINK not in post_link and BASE_LINK2 not in post_link:
    post_link = input('Please Input A Valid Post Link: ')


# ** This is SO IMPORTANT Because it enables you to
# ** be logged in coursera automatically so that they don't
# ** know you are a bot other wise they will block you
options = webdriver.ChromeOptions()

# ? This will load the cookies and passwords from
# ? the orignal Chrome browser
options.add_argument(
    r"--user-data-dir=C:\Users\karim\AppData\Local\Google\Chrome\User Data")

# ? This will reduse the amount of lines that
# ? Selenium prints to the terminal
options.add_argument('--log-level=3')

# open the browser
browser = webdriver.Chrome(
    executable_path="E:\Progammes\chromedriver_win32\chromedriver.exe",
    options=options)
browser.get(post_link)


time.sleep(2)
# input_fields, buttons = None, None
groups = open(
    "E:\karim\Py_Automate\Facebook Auto Group Posting\groups_names.txt",
    'r',
    encoding='UTF-8')

shown = False

for group_name in groups.readlines():
    if not group_name:
        continue

    group_name = group_name.strip()

    # STEP #1 Press Main Share Button
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Share"))).click()

    # STEP #2 Press share in a group button
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Share in a group"))).click()

    time.sleep(2)
    input_fields = browser.find_elements_by_tag_name('input')

    # STEP #3 Write Group Name Then Share
    ActionChains(browser)\
        .move_to_element(input_fields[-2])\
        .click(input_fields[-2])\
        .click(input_fields[-2])\
        .perform()

    time.sleep(2)
    input_fields[-2].send_keys(group_name[0])
    time.sleep(2)
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

   # STEP #4 press the CheckBox include_original_post if exists
    try:
        ActionChains(browser)\
            .move_to_element(input_fields[-1])\
            .click(input_fields[-1])\
            .perform()
    except:
        print('\n\ninclude_original_post was not found.\n'.title())

    # post_button
    buttons = browser.find_elements_by_tag_name('button')
    buttons[-1].click()
    print(group_name.ljust(85) + '|DONE|' + '\n-----------------')
    time.sleep(6)  # wait sometime until the next share


browser.close()
# sys.exit()
