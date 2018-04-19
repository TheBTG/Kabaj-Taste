"""Class responsible for analyzing the json returned from the server
At the moment, getFoundFood() will only return a valid value if the same
Prop has been seen 3 times in a row with a confidence > .7
"""


class ResponseAnalyzer:
    def __init__(self, threshold, streak_threshold):
        self.streak = 0
        self.streakFood = None
        self.identifiedFood = None
        self.has_been_checked = True
        self.threshold = threshold
        self.streak_threshold = streak_threshold

    # input: response json
    def analyze_response(self, response):
        self.has_been_checked = False
        highest_confidence = 0.0
        highest_entry = ''

        entries = {}

        for key in response.keys():
            if key == "answer":
                for guess in response[key].keys():
                    print(f"guess: {guess}")
                    entries[response[key][guess]] = guess
        for key in entries.keys():
            print(f'{entries[key]}: {key}')
            if key > highest_confidence:
                highest_confidence = key
                highest_entry = entries[key]

        if highest_confidence > self.threshold:
            if highest_entry != 'garbage' and highest_entry == self.streakFood:
                self.streak += 1
                if self.streak >= self.streak_threshold:
                    self.identifiedFood = self.streakFood
                    self.streak = 0
            else:
                self.streakFood = highest_entry
                self.streak = 0

    def getFoundFood(self):
        self.has_been_checked = True
        if self.identifiedFood is not None:
            food = self.identifiedFood
            self.identifiedFood = None
            return food
        else:
            # Occurs when no valid food has been identified
            raise Exception("")

    def has_found_food(self):
        self.has_been_checked = True
        if self.identifiedFood is not None:
            return True
        else:
            return False
