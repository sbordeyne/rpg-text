class Calendar:
    months = ["jasocus",
              "frahocus",
              "warrs",
              "asons",
              "doqi",
              "jume",
              "jacirs",
              "aurora",
              "sophen",
              "ooqen",
              "nidah",
              "dribah",
              "zyge"]
    days = ["morndas",
            "tirdas",
            "middas",
            "turdas",
            "fredas",
            "loredas",
            "sundas"]
    hours_per_day = 20
    minutes_per_hour = 60
    minutes_per_turn = 10
    days_per_week = 7
    weeks_per_month = 4
    days_per_month = days_per_week * weeks_per_month
    days_per_year = len(months) * days_per_month


class GameTimer:
    def __init__(self, game):
        self.game = game
        self.n_turns = 0
        self.init_time = 540
        self.init_year = 591

    def tick(self, n_ticks=1):
        self.n_turns += n_ticks

    @property
    def date(self):
        game_day = (self.init_time + self.n_turns * Calendar.minutes_per_turn) // \
                   (Calendar.hours_per_day * Calendar.minutes_per_hour)
        month_name = Calendar.months[(game_day // Calendar.days_per_month) % len(Calendar.months)]
        day_number = game_day % Calendar.days_per_month
        weekday_name = Calendar.days[day_number % Calendar.days_per_week]
        year_number = self.init_year + game_day // Calendar.days_per_year
        return f"{weekday_name} the {day_number} of {month_name}, Year X{year_number} at {self.time}"

    @property
    def time(self):
        total_minutes = (self.init_time + self.n_turns * Calendar.minutes_per_turn) // \
                        (Calendar.hours_per_day * Calendar.minutes_per_hour)
        hours = total_minutes % Calendar.minutes_per_hour
        minutes = total_minutes // Calendar.minutes_per_hour
        return f"{hours}:{minutes}"

    def serialize(self):
        return {"n_turns": self.n_turns}

    def deserialize(self, data):
        self.n_turns = data["n_turns"]