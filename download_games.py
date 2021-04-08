# downloading all my chess game
import argparse
import pathlib
from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from stdiomask import getpass

# ---------- arguments ----------
argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("download_dir", nargs="?", default=None, type=pathlib.Path)
argument_parser.add_argument(
    "--user",
    required=False,
    default="",
    type=lambda x: x or input("User: "),
)
argument_parser.add_argument(
    "--password",
    required=False,
    default="",
    type=lambda x: x or getpass("Password: "),
)
args = argument_parser.parse_args()


# ---------- configure the profile ----------
profile = FirefoxProfile()
profile.set_preference("browser.download.panel.shown", False)
profile.set_preference(
    "browser.helperApps.neverAsk.saveToDisk",
    "application/vnd.chess-pgn, application/x-chess-pgn",
)
profile.set_preference("browser.download.folderList", 2)
if args.download_dir is not None:
    args.download_dir.mkdir(parents=True, exist_ok=True)
    profile.set_preference("browser.download.dir", str(args.download_dir.absolute()))

# ---------- start the browser ----------
with webdriver.Firefox(firefox_profile=profile) as browser:
    browser.implicitly_wait(5)

    # ---------- log in ----------
    browser.get("https://www.chess.com")
    log_page = browser.find_elements_by_xpath(
        '//*[contains(concat( " ", @class, " " ), concat( " ", "login", " " ))]'
    )
    log_page[0].click()
    login_link = browser.find_element_by_name("_username")
    pass_link = browser.find_element_by_name("_password")
    login_link.send_keys(args.user)
    pass_link.send_keys(args.password)
    login_btt = browser.find_element_by_xpath("//button[@type='submit']")
    login_btt.click()

    # ---------- download the games ----------
    browser.get("https://www.chess.com/games/archive?gameOwner=my_game&gameType=live")

    while True:
        check_all = browser.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "archive-games-check-all", " " ))]')
        check_all.click()
        download = browser.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "v-tooltip", " " ))]')
        download.click()
        sleep(0.5)
        next_page = browser.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "pagination-next", " " ))]')

        try:
            next_page.click()
        except:
            break
