import datetime
import os

class GameStatistics():
    """
    Collects statistics from the game upon finishing the game
    """
    def __init__(self, gamestate):
        self.player = gamestate.player
        self.campaign_name = gamestate.campaign_name

        # Generated
        self.directory = os.path.join('.', 'statistics')
        os.makedirs(self.directory, exist_ok=True)
        self.filename = os.path.join(self.directory, f"{gamestate.campaign_name}.txt")
        # End generation

    def write_stats(self):
        try:
            current_date = datetime.date.today()
            score_entry = f"{current_date} - {self.player.score}\n"
            print("Writing stats: ", score_entry)

            with open(self.filename, 'a', encoding='utf-8') as file:
                file.write(score_entry)
        except ReferenceError as e:
            print ("ERROR: ",e)
