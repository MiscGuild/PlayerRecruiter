import asyncio
from math import sqrt

import aiohttp

import settings


async def get_hyapi_key():
    return settings.API_KEY


# Base JSON-getter for all JSON based requests. Catches Invalid API Key errors
async def get_json_response(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp = await resp.json(content_type=None)
            await session.close()

    if not resp:
        return None

    # Return JSON response
    return resp


async def get_mojang_profile(name: str):
    resp = await get_json_response(f"https://api.mojang.com/users/profiles/minecraft/{name}")
    # If player and request is valid
    if resp and ("errorMessage" not in resp) and ("name" in resp):
        return resp["name"], resp["id"]
    api_key = await get_hyapi_key()
    resp = await get_json_response(f"https://api.hypixel.net/player?key={api_key}&name={name}")
    if resp and 'player' in resp and resp['player']:
        return resp['player']['displayname'], resp['player']['uuid']

    # Player does not exist
    return None, None


async def get_hypixel_player(name: str = None, uuid: str = None):
    api_key = await get_hyapi_key()
    if uuid:
        resp = await get_json_response(f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}")
    else:
        resp = await get_json_response(f"https://api.hypixel.net/player?key={api_key}&name={name}")

    # Player doesn't exist
    if "player" not in resp or not resp["player"]:
        return None

    # Player exists
    return resp["player"]


async def get_name_by_uuid(uuid: str):
    i = 0
    while i < 5:
        i += 1
        resp = await get_json_response(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
        # Player does not exist
        if not resp:
            continue

        return resp["name"]
    api_key = await get_hyapi_key()
    # If the Mojang API fails to return a name, the bot checks using the hypixel API
    resp = await get_json_response(f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}")
    if "player" not in resp:
        return None
    return resp['player']['displayname']


def session_get_name_by_uuid(session, uuid):
    with session.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}") as resp:
        data = resp.json()

        if resp.status_code != 200:
            return None
        return data["name"]


async def get_player_guild(uuid):
    api_key = await get_hyapi_key()
    resp = await get_json_response(f"https://api.hypixel.net/guild?key={api_key}&player={uuid}")

    # Player is not in a guild
    if "guild" not in resp or not resp["guild"]:
        if "throttle" in resp:
            return "API Throttle"
        return None

    # Player is in a guild
    return resp["guild"]


async def get_guild_by_name(name):
    api_key = await get_hyapi_key()
    resp = await get_json_response(f"https://api.hypixel.net/guild?key={api_key}&name={name}")

    # Player is not in a guild
    if "guild" not in resp or not resp["guild"]:
        return None

    # Player is in a guild
    return resp["guild"]


async def get_guild_uuids(guild_name: str):
    resp = await get_guild_by_name(guild_name)
    if not resp:
        return None
    return [member["uuid"] for member in resp["members"]]


async def get_gtag(name):
    api_key = await get_hyapi_key()
    resp = await get_json_response(f"https://api.hypixel.net/guild?key={api_key}&name={name}")

    if len(resp["guild"]) < 2:
        return (" ")
    if not resp["guild"]["tag"]:
        return (" ")
    gtag = resp["guild"]["tag"]
    return (f"[{gtag}]")


async def get_guild_level(exp):
    EXP_NEEDED = [100000, 150000, 250000, 500000, 750000, 1000000, 1250000, 1500000, 2000000, 2500000, 2500000, 2500000,
                  2500000, 2500000, 3000000]
    # A list of amount of XP required for leveling up in each of the beginning levels (1-15).

    level = 0

    for i in range(1000):
        # Increment by one from zero to the level cap.
        need = 0
        if i >= len(EXP_NEEDED):
            need = EXP_NEEDED[len(EXP_NEEDED) - 1]
        else:
            need = EXP_NEEDED[i]
        # Determine the current amount of XP required to level up,
        # in regards to the "i" variable.

        if (exp - need) < 0:
            return round(((level + (exp / need)) * 100) / 100, 2)
        # If the remaining exp < the total amount of XP required for the next level,
        # return their level using this formula.

        level += 1
        exp -= need
        # Otherwise, increase their level by one,
        # and subtract the required amount of XP to level up,
        # from the total amount of XP that the guild had.


async def get_rank(uuid):
    player = await get_hypixel_player(uuid=uuid)
    if player is None:
        return None
    if "newPackageRank" in player:
        rank = (player["newPackageRank"])
        if rank == 'MVP_PLUS':
            if "monthlyPackageRank" in player:
                mvp_plus_plus = (player["monthlyPackageRank"])
                if mvp_plus_plus == "NONE":
                    return '[MVP+]'
                return "[MVP++]"
            return "[MVP+]"
        if rank == 'MVP':
            return '[MVP]'
        if rank == 'VIP_PLUS':
            return 'VIP+'
        if rank == 'VIP':
            return '[VIP]'

    return None


async def check_skywars_requirements(player_data):
    if not player_data:
        return False
    if "stats" not in player_data:
        return False
    if "SkyWars" not in player_data["stats"]:
        return False
    if "Wins" not in player_data["stats"]["SkyWars"]:
        return False
    if "levelFormatted" not in player_data["stats"]["SkyWars"]:
        return False

    level = int(player_data["stats"]["SkyWars"]["levelFormatted"][2:-1])
    wins = int(player_data["stats"]["SkyWars"]["Wins"])

    if (level > settings.SKYWARS_LEVEL) and (wins > settings.SKYWARS_WINS):
        return True

    return False


async def check_bedwars_requirements(player_data):
    if not player_data:
        return False
    if "stats" not in player_data:
        return False
    if "achievements" not in player_data:
        return False
    if "Bedwars" not in player_data["stats"]:
        return False
    if "bedwars_level" not in player_data["achievements"]:
        return False
    if "wins_bedwars" not in player_data["stats"]["Bedwars"]:
        return False
    if "final_kills_bedwars" not in player_data["stats"]["Bedwars"]:
        return False
    if "final_deaths_bedwars" not in player_data["stats"]["Bedwars"]:
        return False

    star = player_data["achievements"]["bedwars_level"]
    wins = int(player_data["stats"]["Bedwars"]["wins_bedwars"])
    final_kills = int(player_data["stats"]["Bedwars"]["final_kills_bedwars"])
    final_deaths = int(player_data["stats"]["Bedwars"]["final_deaths_bedwars"])
    fkdr = final_kills / final_deaths
    index = star * pow(fkdr, 2)

    if (wins > settings.BEDWARS_WINS) and (fkdr > settings.BEDWARS_FKDR) and (index > settings.BEDWARS_INDEX) and (star >= settings.BEDWARS_STARS):
        return True

    return False


async def check_duels_requirements(player_data):
    if not player_data:
        return False
    if "stats" not in player_data:
        return False
    if "Duels" not in player_data["stats"]:
        return False
    if "wins" not in player_data["stats"]["Duels"]:
        return False
    if "losses" not in player_data["stats"]["Duels"]:
        return False

    wins = int(player_data["stats"]["Duels"]["wins"])
    losses = int(player_data["stats"]["Duels"]["losses"])
    wlr = wins / losses

    if (wins > settings.DUELS_WINS) and (wlr > settings.DUELS_WLR):
        return True

    return False


async def check_arcade_requirements(player_data):
    if not player_data:
        return False
    if "stats" not in player_data:
        return False
    if "achievements" not in player_data:
        return False
    if "Arcade" not in player_data["stats"]:
        return False
    if "arcade_arcade_winner" not in player_data["achievements"]:
        return False

    wins = int(player_data["achievements"]["arcade_arcade_winner"])

    if wins > settings.ARCADE_WINS:
        return True

    return False


async def check_murdermystery_requirements(player_data):
    if not player_data:
        return False
    if "stats" not in player_data:
        return False
    if "MurderMystery" not in player_data["stats"]:
        return False
    if "wins" not in player_data["stats"]["MurderMystery"]:
        return False

    wins = int(player_data["stats"]["MurderMystery"]["wins"])

    if wins > settings.MURDER_MYSTERY_WINS:
        return True

    return False


async def check_network_level_requirements(player_data):
    if not player_data:
        return False
    if "networkExp" not in player_data:
        return False

    level = (sqrt((2 * player_data["networkExp"]) + 30625) / 50) - 2.5

    if level > settings.NETWORK_LEVEL:
        return True

    return False


async def check_gexp_requirements(guild_data, uuid):
    if guild_data:
        for member in guild_data["members"]:
            if member["uuid"] == uuid:
                gexp = sum(member["expHistory"].values())

        if gexp > settings.MINIMUM_GEXP:
            return True

    return False


async def check_max_guild_level(guild_data):
    if guild_data:
        if (await get_guild_level(guild_data["exp"])) > settings.MAXIMUM_GUILD_LEVEL:
            return True

    return False


async def check_if_meets_requirements(username):
    meets_requirements = False
    guildless = False
    error = False

    name, uuid = await get_mojang_profile(username)
    if name == None:
        await asyncio.sleep(60)

        name, uuid = await get_mojang_profile(username)

    player_data = await get_hypixel_player(name=username, uuid=uuid)
    if not player_data:
        return None, None, True

    meets_skywars_requirements = await check_skywars_requirements(player_data)
    meets_bedwars_requirements = await check_bedwars_requirements(player_data)
    meets_duels_requirements = await check_duels_requirements(player_data)
    meets_arcade_requirements = await check_arcade_requirements(player_data)
    meets_murderymystery_requirements = await check_murdermystery_requirements(player_data)

    if any([meets_skywars_requirements, meets_bedwars_requirements, meets_duels_requirements, meets_arcade_requirements,
            meets_murderymystery_requirements]):
        meets_requirements = True

    if meets_requirements:
        guild_data = await get_player_guild(uuid)
        if not guild_data:
            guildless = True
        elif guild_data == "API Throttle":
            guildless = False
            return guildless, meets_requirements, error
        else:
            meets_gexp_requirements = await check_gexp_requirements(guild_data, uuid)
            meets_max_guild_level = await check_max_guild_level(guild_data)
            if not meets_gexp_requirements:
                meets_requirements = False
            if meets_max_guild_level:
                meets_requirements = False
    return guildless, meets_requirements, error
