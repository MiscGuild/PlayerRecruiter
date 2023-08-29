import json
import os


def init():
    config = getSettings()

    API_KEY = config["API_KEY"]
    PATH = config["PATH"]
    SKYWARS_WINS = config["REQUIREMENTS"]["SKYWARS_WINS"]
    SKYWARS_LEVEL = config["REQUIREMENTS"]["SKYWARS_LEVEL"]
    BEDWARS_STARS = config["REQUIREMENTS"]["BEDWARS_STARS"]
    BEDWARS_WINS = config["REQUIREMENTS"]["BEDWARS_WINS"]
    BEDWARS_INDEX = config["REQUIREMENTS"]["BEDWARS_INDEX"]
    BEDWARS_FKDR = config["REQUIREMENTS"]["BEDWARS_FKDR"]
    DUELS_WINS = config["REQUIREMENTS"]["DUELS_WINS"]
    DUELS_WLR = config["REQUIREMENTS"]["DUELS_WLR"]
    ARCADE_WINS = config["REQUIREMENTS"]["ARCADE_WINS"]
    MURDER_MYSTERY_WINS = config["REQUIREMENTS"]["MURDER_MYSTERY_WINS"]
    MINIMUM_GEXP = config["REQUIREMENTS"]["MINIMUM_GEXP"]
    MAXIMUM_GUILD_LEVEL = config["REQUIREMENTS"]["MAXIMUM_GUILD_LEVEL"]
    NETWORK_LEVEL = config["REQUIREMENTS"]["NETWORK_LEVEL"]
    globals().update(locals())


def getSettings():
    user_home = os.path.expanduser("~")
    User_Profile = os.getenv('USERPROFILE')
    documents_path = os.path.join(user_home, 'Documents')
    folder_name = "MiscRecruitment"
    folder_path = os.path.join(documents_path, folder_name)
    file_name = "config.json"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

        json_data = {
            "API_KEY": "",
            "PATH": fr'{User_Profile}\.lunarclient\offline\multiver\logs\latest.log',
            "REQUIREMENTS": {
                "SKYWARS_WINS": 0,
                "SKYWARS_LEVEL": 0,
                "BEDWARS_STARS": 0,
                "BEDWARS_WINS": 0,
                "BEDWARS_INDEX": 0,
                "BEDWARS_FKDR": 0,
                "DUELS_WINS": 0,
                "DUELS_WLR": 0,
                "ARCADE_WINS": 0,
                "MURDER_MYSTERY_WINS": 0,
                "MINIMUM_GEXP": 0,
                "MAXIMUM_GUILD_LEVEL": 999,
                "NETWORK_LEVEL": 0
            }
        }

        with open(os.path.join(folder_path, file_name), 'w') as f:
            json.dump(json_data, f)
            config = json.load(f)
            return config

    with open(os.path.join(folder_path, file_name), 'r') as f:
        config = json.load(f)

    return config


def updateSettings(API_KEY, PATH, SKYWARS_WINS, SKYWARS_LEVEL, BEDWARS_STARS, BEDWARS_WINS, BEDWARS_INDEX, BEDWARS_FKDR,
                   DUELS_WINS, DUELS_WLR, ARCADE_WINS, MURDER_MYSTERY_WINS, MINIMUM_GEXP,
                   MAXIMUM_GUILD_LEVEL, NETWORK_LEVEL):
    user_home = os.path.expanduser("~")
    User_Profile = os.getenv('USERPROFILE')
    documents_path = os.path.join(user_home, 'Documents')
    folder_name = "MiscRecruitment"
    folder_path = os.path.join(documents_path, folder_name)
    file_name = "config.json"

    paths_dict = {
        "Lunar Client": fr'{User_Profile}\.lunarclient\offline\multiver\logs\latest.log',
        "Badlion Client": fr'{User_Profile}\AppData\Roaming\.minecraft\logs\blclient\minecraft\latest.log',
        "Feather Client": fr'{User_Profile}\AppData\Roaming\.minecraft\logs\latest.log',
        "Vanilla": fr'{User_Profile}\AppData\Roaming\.minecraft\logs\latest.log'
    }

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    json_data = {
        "API_KEY": API_KEY,
        "PATH": paths_dict.get(PATH),
        "REQUIREMENTS": {
            "SKYWARS_WINS": SKYWARS_WINS,
            "SKYWARS_LEVEL": SKYWARS_LEVEL,
            "BEDWARS_STARS": BEDWARS_STARS,
            "BEDWARS_WINS": BEDWARS_WINS,
            "BEDWARS_INDEX": BEDWARS_INDEX,
            "BEDWARS_FKDR": BEDWARS_FKDR,
            "DUELS_WINS": DUELS_WINS,
            "DUELS_WLR": DUELS_WLR,
            "ARCADE_WINS": ARCADE_WINS,
            "MURDER_MYSTERY_WINS": MURDER_MYSTERY_WINS,
            "MINIMUM_GEXP": MINIMUM_GEXP,
            "MAXIMUM_GUILD_LEVEL": MAXIMUM_GUILD_LEVEL,
            "NETWORK_LEVEL": NETWORK_LEVEL,
        }
    }

    with open(os.path.join(folder_path, file_name), 'w') as f:
        json.dump(json_data, f)

    init()
