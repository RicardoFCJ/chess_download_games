# downloading all my chess game
import argparse
import glob
import os
import pathlib
from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from stdiomask import getpass

PAGE_FILENAME_GLOB = "chess_com_games*"


def set_string_preference(driver, name, value):
    driver.execute_script("window.open()")
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])

    driver.get("about:config")
    driver.execute_script(
        """
    var prefs = Components.classes["@mozilla.org/preferences-service;1"]
        .getService(Components.interfaces.nsIPrefBranch);
    prefs.setCharPref(arguments[0], arguments[1]);
    """,
        name,
        value,
    )

    driver.close()
    driver.switch_to.window(windows[-2])


def merge_pages(*files, out):
    with open(out, "w") as out:
        for path in files:
            with open(path) as page:
                out.write(page.read())
                out.write("\n")
            os.remove(path)


# ---------- arguments ----------
argument_parser = argparse.ArgumentParser()
argument_parser.add_argument(
    "download_dir",
    nargs="?",
    default=".",
    type=pathlib.Path,
    help="The download directory; defaults to the current working directory.",
)
argument_parser.add_argument(
    "--concatenate",
    action="store_true",
    default=True,
    help="Concatenate all files containing a single page of games into one big file. "
    "Each of the individual pages is then discarded. If --separate-types is set, two "
    "files are created: `live.pgn` and `daily.pgn`. Otherwise, a single `games.pgn` "
    "file is created. This is set by default.",
)
argument_parser.add_argument(
    "--dont-concatenate",
    action="store_false",
    dest="concatenate",
    help="The opposite of --concatenate. Each page is downloaded as a single file.",
)
argument_parser.add_argument(
    "--separate-types",
    action="store_true",
    help="Separate game files into live games and daily games. "
    "If --concatenate is set (default), a `live.pgn` file and a `daily.pgn` file are "
    "created in the download directory. If --dont-concatenate is set, pages for live "
    "and daily games are downloaded in the `live/` and `daily/` subdirectories "
    "(within the download directory) respectively.",
)
argument_parser.add_argument(
    "--user",
    required=False,
    default="",
    type=lambda x: x or input("User: "),
    help="The chess.com username for the user whose games are to be downloaded. If not "
    "provided, it will be asked interactively.",
)
argument_parser.add_argument(
    "--password",
    required=False,
    default="",
    type=lambda x: x or getpass("Password: "),
    help="The chess.com password for the user whose games are to be downloaded. If not "
    "provided, it will be asked interactively.",
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

    # ---------- download each page ----------
    # note previously existing files to avoid using them or deleting them
    existing_files = set(glob.glob(str(args.download_dir / PAGE_FILENAME_GLOB)))

    for game_type in "live", "daily":
        browser.get(f"https://www.chess.com/games/archive?gameOwner=my_game&gameType={game_type}")

        if args.separate_types and not args.concatenate:
            subdir: pathlib.Path = args.download_dir / game_type
            subdir.mkdir(parents=True, exist_ok=True)
            set_string_preference(
                browser, "browser.download.dir", str(subdir.absolute())
            )
            existing_files = set(glob.glob(str(subdir / PAGE_FILENAME_GLOB)))

        while True:
            check_all = browser.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "archive-games-check-all", " " ))]')
            check_all.click()
            download = browser.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "v-tooltip", " " ))]')
            download.click()
            sleep(0.5)

            try:
                next_page = browser.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "pagination-next", " " ))]')
                next_page.click()
            except:
                break

        # ---------- concatenate pages into one file ----------
        if args.separate_types and args.concatenate:
            paths = sorted(
                set(glob.glob(str(args.download_dir / PAGE_FILENAME_GLOB)))
                - existing_files,
                key=os.path.getmtime,
            )
            merge_pages(*paths, out=args.download_dir / f"{game_type}.pgn")

    if not args.separate_types and args.concatenate:
        paths = sorted(
            set(glob.glob(str(args.download_dir / PAGE_FILENAME_GLOB)))
            - existing_files,
            key=os.path.getmtime,
        )
        merge_pages(*paths, out=args.download_dir / f"games.pgn")
