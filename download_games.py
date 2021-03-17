#downloading all my chess game
from stdiomask import getpass
user = input("User: ")
key = getpass("Password: ")
import pathlib
from time import sleep
from selenium import webdriver
#from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

#pathlib.Path('./games/').mkdir(parents=True, exist_ok=True)
profile = FirefoxProfile()
profile.set_preference("browser.download.panel.shown", False)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/vnd.chess-pgn, application/x-chess-pgn')
profile.set_preference("browser.download.folderList", 2)
#profile.set_preference("browser.download.dir", "~/Projects/chess_download_games/games/")
browser = webdriver.Firefox(firefox_profile=profile)

browser.implicitly_wait(5)

browser.get('https:www.chess.com')
log_page = browser.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "login", " " ))]')
log_page[0].click()

login_link = browser.find_element_by_name("_username")
pass_link = browser.find_element_by_name("_password")
login_link.send_keys(user)
pass_link.send_keys(key)

login_btt = browser.find_element_by_xpath("//button[@type='submit']")
login_btt.click()

browser.get("https://www.chess.com/games/archive?gameOwner=my_game&gameTypes%5B0%5D=chess960&gameTypes%5B1%5D=daily&gameType=live")

while(True):
    check_all = browser.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "archive-games-check-all", " " ))]')
    check_all.click()
    download = browser.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "v-tooltip", " " ))]')
    download.click()
    sleep(2)
    next_page = browser.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "pagination-next", " " ))]')
    
    try:
        next_page.click()
        sleep(2)
    except:
        browser.close()
        exit()