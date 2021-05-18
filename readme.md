# MLB Team Game Status PolyBar Module
This is a lightweight script intended for use with polybar.
It displays game status for a given team. If a game is in progress, it displays the score and the inning. Otherwise, it displays the date and time of the next game, and the opposing team name.

## Usage
Clone the repo and install the requirements into a virtual environment.
Edit the main python file with desired team and time zone. 

Add the following to your polybar config:
```
[module/mlb]
type = custom/script
exec = <path-to-mlb-dir>/venv/bin/python <path-to-mlb-dir>/mlb-test.py
interval = 120
```

By default, this updates every 2 minutes. Edit as needed.