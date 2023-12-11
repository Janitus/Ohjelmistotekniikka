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

    def get_top_scores(self, top_amount=5):
        """
        Reads the statistics file and returns the top N scores.
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            score_entries = []
            for line in lines:
                parts = line.strip().split(' - ')
                if len(parts) == 2:
                    date_str, score_str = parts
                    try:
                        score = int(score_str)
                        score_entries.append((date_str, score))
                    except ValueError:
                        print(f"Invalid score format in line: {line}")

            # Generated
            score_entries.sort(key=lambda x: x[1], reverse=True)
            top_scores = score_entries[:top_amount]
            # End generate

            return top_scores

        except FileNotFoundError:
            print(f"File not found: {self.filename}")
            return []
