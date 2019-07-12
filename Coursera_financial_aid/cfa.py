import pyautogui
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
import time
from pprint import pprint
from bs4 import BeautifulSoup
import pyautogui
from selenium.webdriver.common.by import By
import selenium.common.exceptions as sel_exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_LINK = 'https://www.coursera.org'
TEST_LINK = 'https://www.coursera.org/specializations/applied-data-science'
pyautogui.PAUSE = 1

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

browser = webdriver.Chrome(
    executable_path="E:\Progammes\chromedriver_win32\chromedriver.exe", chrome_options=options)


def prepare_links():
    link = TEST_LINK

    # Getting the link as a terminal argument
    # or as user input
    while not link:
        if len(sys.argv) < 2:
            link = input(
                'I see you forgot to enter the coursera link.\nPlease, enter it:').strip()
        else:
            link = sys.argv[1]

    print('\nConnecting...\n' + '#'*50)
    req = requests.get(link)
    req.raise_for_status()
    soup = BeautifulSoup(req.text, 'html.parser')
    title = soup.select('h1')[1].getText()
    # .select('href'))  # .getText())

    if 'specializations' in link:
        print('\nSpecialization Title: %s' % title)
        return get_spec_courses(soup, title)
    else:
        print('Course Title: %s\n' % title + '#'*50)
        return [link]


def get_spec_courses(soup, spec_title):
    all = soup.find_all('a', attrs={'data-e2e': "course-link"})
    # A list of two lists:
    # the the list at index [0] contains courses names
    # the the list at index [1] contains courses linkss
    names_links = [[], []]
    # file = open('%s.txt' % spec_title, 'w')
    for course in all:
        course_link = BASE_LINK + course.get('href')
        course_name = course.select('h3')[0].getText()
        names_links[0].append(course_name)
        names_links[1].append(course_link)
    print('_' * 90, '\n')
    return names_links


def fill_first_page(link):
    global browser
    # Openning Link
    browser.get(link)

    # Pressing on the financial aid button
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "finaid_button"))).click()

    # Watting for the pop-up box to appear
    time.sleep(1)

    # Pressing the Button | Continue to the forum |
    browser.find_element_by_id('financial_aid_modal_apply_button').click()

    # Watting until the page is loaded to check the boxes
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "info_checkbox"))).click()
    browser.find_element_by_id('completion_checkbox').click()

    # Inputting text to text field
    browser.find_element_by_id(
        'accept-terms-field').send_keys('I agree to the terms above')

    # Clicking the button to go to the final page
    browser.find_element_by_id('continue_finaid_application_button').click()


def fill_final_page():
    global browser

    # Preparing the answers
    ans = open('coursera_answers.txt').read().split('##')

    # Education dropbox >> Student
    browser.find_element_by_id(
        'finaid-educationalBackground').send_keys(Keys.DOWN)
    # Income per Year >> 10$
    browser.find_element_by_id(
        'finaid-income').send_keys('10')
    # Employment Status >> Student
    browser.find_element_by_id(
        'finaid-employmentStatus').send_keys([Keys.DOWN]*4)
    # Money You can pay per month >> 1$
    browser.find_element_by_id(
        'finaid-amount-can-pay').send_keys('1')
    # Answer to Question >> Why are you applying for Financial Aid?
    browser.find_element_by_id(
        'finaid-reason').send_keys(ans[0])

    # Answer to Question
    # >> How will taking this course help you achieve your career goals?
    browser.find_element_by_id(
        'finaid-goal').send_keys(ans[1])

    # Answer to Question >> Help Us Improve  : NO
    last_field = browser.find_element_by_id(
        'finaid-loanReason')
    last_field.send_keys(ans[2])

    # TODO Add the submit code
    # last_field.submit()


def fill_the_form_for(link):
    fill_first_page(link)
    fill_final_page()


start = time.time()

titles_links = prepare_links()
i = 0
for title, link in zip(titles_links[0], titles_links[1]):
    print('Working On...\n\t\tThe Course: %s\n\t\tLink: %s' % (title, link))

    try:
        fill_the_form_for(link)
        print("\t\tApplying For This Course Is: DONE ✅ ✅ ✅")
        print('#' * 50, '\n')
        i += 1
    except sel_exceptions.NoSuchWindowException:
        browser = webdriver.Chrome(
            executable_path="E:\Progammes\chromedriver_win32\chromedriver.exe", chrome_options=options)

        print(
            '\nThe Browser was Closed. ❌ ❌ ❌' +
            '\n\nReopenning The Browser...\n\n' +
            'Moving To The Next Course...\n\n')

    except Exception as err:
        print('%' * 50)
        print('\nSomeThing Went Wrong! ❌ ❌ ❌\n')
        print('With Course:\n\t%s\n\t%s' % (title, link))
        print('\nSo I Skipped It And Moved To The Next Course\n\n')
        print('The error message:\n%s' % err)
        continue


print(
    '\n\t\t>---->>>>> Finished Applying For', i,
    'Of', len(titles_links[0]),
    'Courses In %s Min.<<<<----<'
    % (round((time.time() - start) / 60, 2)))
browser.quit()
