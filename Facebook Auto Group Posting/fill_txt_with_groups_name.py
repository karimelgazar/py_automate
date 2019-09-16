"""
This scripts fill a txt file with
all the groups my page joined
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

LINE_SEP = '-' * 80
groups_link = 'https://www.facebook.com/pg/karimCodes/groups/?ref=page_internal'
groups_name_css_selector = 'div._3lkd > a > div'


# ** This is SO IMPORTANT Because it enables you to
# ** be logged in coursera automatically so that they don't
# ** know you are a bot other wise they will block you
options = webdriver.ChromeOptions()

# ? This will load the cookies and passwords from
# ? the orignal Chrome browser
options.add_argument(
    r"--user-data-dir=E:\karim\Important\AutomationProfile")

# ? This will reduse the amount of lines that
# ? Selenium prints to the terminal
options.add_argument("--start-maximized")
options.add_argument('--log-level=3')

# open the browser
browser = webdriver.Chrome(
    executable_path="E:\Progammes\chromedriver_win32\chromedriver.exe",
    options=options)

browser.get(groups_link)
groups = browser.find_elements_by_css_selector(groups_name_css_selector)

txt = open("E:\karim\Py_Automate\Facebook Auto Group Posting\\" +
           'groups_names.txt', 'w', encoding='UTF-8')
print(LINE_SEP,
      'Working...',
      LINE_SEP, sep='\n')
for group in groups:
    txt.write(group.text + '\n')

browser.close()
