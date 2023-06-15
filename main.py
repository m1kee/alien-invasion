import datetime

import alien_invasion
import settings
import traceback

try:
    # create an instance of the game and execute it
    settings = settings.Settings()
    ai = alien_invasion.AlienInvasion(settings)
    ai.run_game()
except Exception as e:
    with open('exceptions.log', 'w') as file:
        file.write(traceback.format_exc())
