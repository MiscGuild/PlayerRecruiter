import asyncio
import re
import utils.settings as settings
from threading import Thread

from utils.request_utils import check_if_meets_requirements


# Credits to https://github.com/Were-Woof/Lobby-Stat-Check for the below code
class checkPlayer(Thread):
    def __init__(self, player) -> None:
        super().__init__()
        self.player = player
        self.guildless = []
        self.meets_requirements = []
        self.error = []

    def run(self) -> None:
        guildless, meets_requirements, error = asyncio.run(check_if_meets_requirements(self.player))
        if guildless and meets_requirements:
            self.guildless.append(self.player)
        elif meets_requirements:
            self.meets_requirements.append(self.player)
        elif error:
            self.error.append(self.player)


async def grabChat():
    # Opening the logs file
    players = None
    with open(settings.FULL_PATH, 'r+b') as file:
        for line_bytes in file.readlines():
            line = str(line_bytes).split('[CHAT] ')[-1]  # Only message content
            line = re.sub(r'\\[nrt]', '', line)  # Remove all escape characters

            if line.startswith('Online Players'):
                line = line.split(': ')[-1]  # Players only in message
                players = line.split(', ')  # Split at comma and remove whitespace before name
    if not players:
        return None, None, None, None

    players[-1] = players[-1][:-1]

    # Initializing the threads
    threads = [checkPlayer(player.split('] ')[-1]) for player in players]

    # Starting all the threads
    [t.start() for t in threads]

    # waiting for the threads to complete
    [t.join() for t in threads]

    # Save the values
    all = [player.split('] ')[-1] for player in players]
    guildless = [t.guildless[0] if t.guildless else "" for t in threads]
    meets_requirements = [t.meets_requirements[0] if t.meets_requirements else "" for t in threads]
    error = [t.error[0] if t.error else "" for t in threads]
    return all, guildless, meets_requirements, error
