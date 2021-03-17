# chess_download_games
This script will download all your chess.com live games

You'll need python3 and Firefox installed.

1. Install selenium

python3 -m pip install selenium

2. Download, unpack, and move geckodriver (for linux):

wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz

tar -xvzf geckodriver*

chmod +x geckodriver

sudo mv geckodriver /usr/local/bin/


2.1. (Windows users, have a look here):

https://www.geeksforgeeks.org/how-to-install-selenium-in-python/

3. running the script:

python3 download_games.py

#your games will be saved in firefox's default download directory, unless you uncomment the lines 11 and 16 (linux users only), in which case a folder with the name 'games' will save the files.
