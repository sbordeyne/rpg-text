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
    def game_day(self):
        return (self.init_time + self.n_turns * Calendar.minutes_per_turn) // \
               (Calendar.hours_per_day * Calendar.minutes_per_hour)

    @property
    def month_number(self):
        return (self.game_day // Calendar.days_per_month) % len(Calendar.months) + 1

    @property
    def month_name(self):
        return Calendar.months[self.month_number - 1]

    @property
    def day_number(self):
        return self.game_day % Calendar.days_per_month + 1

    @property
    def day_number_suffix(self):
        if int(str(self.day_number)[-1]) == 1:
            return 'st'
        elif int(str(self.day_number)[-1]) == 2:
            return 'nd'
        elif int(str(self.day_number)[-1]) == 3:
            return 'rd'
        else:
            return 'th'

    @property
    def weekday_name(self):
        return Calendar.days[(self.day_number - 1) % Calendar.days_per_week]

    @property
    def year_number(self):
        return self.init_year + self.game_day // Calendar.days_per_year

    @property
    def date(self):
        return f"{self.weekday_name.capitalize()} the {self.day_number}{self.day_number_suffix} of " \
               f"{self.month_name.capitalize()}, Year X{self.year_number} at {self.time}"

    @property
    def short_date(self):
        return f'{self.day_number}-{self.month_number}-X{self.year_number} @ {self.time}'

    @property
    def time(self):
        total_minutes = (self.init_time + self.n_turns * Calendar.minutes_per_turn) % \
                        (Calendar.hours_per_day * Calendar.minutes_per_hour)
        hours = total_minutes % Calendar.minutes_per_hour
        minutes = total_minutes // Calendar.minutes_per_hour
        return f"{hours:02}:{minutes:02}"

    def serialize(self):
        return {"n_turns": self.n_turns}

    def deserialize(self, data):
        self.n_turns = data["n_turns"]
