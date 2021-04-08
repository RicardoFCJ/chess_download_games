# chess_download_games
This script will download all your chess.com games (both live and daily).

You'll need python3 and Firefox installed.

1. Install selenium
   ```bash
   python3 -m pip install selenium
   ```

2. Download, unpack, and move geckodriver (for linux):
   ```bash
   wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
   tar -xvzf geckodriver*
   chmod +x geckodriver
   sudo mv geckodriver /usr/local/bin/
   ```
   (Windows users, have a look [here](https://www.geeksforgeeks.org/how-to-install-selenium-in-python/).)

3. Run the script:
   ```bash
   python3 download_games.py
   ```

By default, the games will be saved in the current working directory. 
To specify a download directory, pass an argument to the script, e.g. 
`python3 download_games.py ./games`. 
By default, both live and daily games will be saved into a single `games.pgn` file;
if you want to keep each separate, pass the `--separate-types` flag.

For more options and details on the command line interface, run
```shell
python3 download_games.py --help
```
