import statsapi
from datetime import datetime, timedelta
from pytz import UTC, timezone
from dateutil import parser

TEAM_NAME = 'nym'
TZ = timezone('US/Eastern')
OUT_DATE_FORMAT = '%m-%d %I:%m'
OUT_TIME_FORMAT = '%I:%m'

# game_id
# game_datetime
# game_date
# game_type
# status
# away_name
# home_name
# away_id
# home_id
# doubleheader
# game_num
# home_probable_pitcher
# away_probable_pitcher
# home_pitcher_note
# away_pitcher_note
# away_score
# home_score
# current_inning
# inning_state
# venue_id
# venue_name
# summary

# don't touch below here
API_DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
NOW = UTC.localize(datetime.utcnow())

found_teams = statsapi.lookup_team(TEAM_NAME)
team_id = None

if len(found_teams) != 1:
    print('no teams found or too many found')
else:
    team_id = found_teams[0]['id']

schedule = statsapi.schedule(
    start_date=datetime.today().strftime("%Y-%m-%d"), 
    end_date=(datetime.today() + timedelta(days=10)).strftime("%Y-%m-%d"),
    team=team_id
)


def is_utc_date_in_future(date_str):
    try:
        gametime = parser.parse(date_str)
        return gametime > NOW
    except Exception as e:
        print(f'Woops, exception: {e}')


next_game = None
next_game_date = None
in_progress = False
while True:
    if (len(schedule) < 1):
        print('outta games yo')

    next_game = schedule.pop(0)
    next_game_date = next_game['game_datetime']
    if is_utc_date_in_future(next_game_date):
        break
    else:
        if (next_game['status'] != 'Final'):
            in_progress = True
            break

opponent_id = None
at_home = False
if (next_game['away_id'] == team_id):
    opponent_id = next_game['home_id']
    at_home = False
else:
    opponent_id = next_game['away_id']
    at_home = True


def is_tonight(date):
    return date.day == NOW.day and date.hour >= 18


def is_today(date):
    return date.day == NOW.day and date.hour < 18


def get_day(date):
    return parser.parse(date).day
    # return date.day


def get_game_time_str(game):
    return UTC.localize(
            datetime.strptime(game['game_datetime'], 
            API_DATE_FORMAT)
        ).astimezone(TZ).strftime(OUT_TIME_FORMAT)


def get_game_datetime_str(game):
    return UTC.localize(
            datetime.strptime(game['game_datetime'], 
            API_DATE_FORMAT)
        ).astimezone(TZ).strftime(OUT_DATE_FORMAT)

prefix_str = ""

next_game_date_datetime = parser.parse(next_game_date)
if is_today(next_game_date_datetime):
    prefix_str = "Today " + get_game_time_str(next_game)
elif is_tonight(next_game_date_datetime):
    prefix_str = "Tonight " + get_game_time_str(next_game)
elif in_progress:
    prefix_str = (
        str(next_game['inning_state']) + 
        " " + 
        str(next_game['current_inning']) +
        " | " + 
        str(next_game['away_score']) + 
        "-" + 
        str(next_game['home_score'])
    )
else:
    prefix_str = get_game_datetime_str(next_game)


def get_team_name(id):
    return statsapi.lookup_team(id).pop(0)['teamName']


teams_str = ""
if at_home:
    teams_str = get_team_name(opponent_id) + " @ " + get_team_name(team_id)
else:
    teams_str = get_team_name(team_id) + " @ " + get_team_name(opponent_id) 


print(prefix_str + " | " + teams_str)
