import datetime

BONUSES = {
    0: 30,
    1: 25,
    2: 25,
    3: 20,
    4: 20,
    5: 15,
    6: 15,
    7: 15,
    8: 15,
    9: 10,
    10: 10,
    11: 10,
    12: 10,
    13: 5,
    14: 5,
    15: 5,
    16: 5,
    17: 0,
    18: 0,
    19: 0,
    20: 0,
    21: 0,
    22: 0,
    23: 0
}

EN_CODE = {
    0: '-',
    1: 'листик2',
    2: 'обеденные3',
    3: 'группы4',
    4: 'прайс5',
    5: 'восемь6',
    6: 'доллар7',
    7: 'памятка8',
    8: 'кухни9',
    9: 'сроки10',
    10: 'условные11',
    11: 'каменка12',
    12: 'мияги13',
    13: 'ощущения14',
    14: 'фонарики15',
    15: 'сотрудничества16',
    16: 'ценно17',
    17: 'луиза18',
    18: 'алекси19',
    19: 'квадратные20',
    20: 'бабочки21',
    21: 'вкладыш22',
    22: 'бука23'
}

EN_BONUS_TIME = {
    0: 0,
    1: 10,
    2: 15,
    3: 20,
    4: 25,
    5: 30,
    6: 40,
    7: 50,
    8: 60,
    9: 80,
    10: 100,
    11: 120,
    12: 150,
    13: 180,
    14: 210,
    15: 250,
    16: 290,
    17: 330,
    18: 380,
    19: 430,
    20: 490,
    21: 550,
    22: 610
}


class Game:
    active = False
    ready = False
    player_id = 0
    level = 0
    end_time = datetime.datetime.now()

    def start(self, player_id):
        self.player_id = player_id
        self.active = True
        self.ready = False
        self.level = 0
        self.end_time = datetime.datetime.now() + datetime.timedelta(seconds=BONUSES[self.level])

    def same_player(self, player_id):
        return self.player_id == player_id

    def level_up(self):
        self.level += 1
        self.end_time += datetime.timedelta(seconds=BONUSES[self.level])

    def check(self):
        if datetime.datetime.now() > self.end_time:
            self.active = False
            return False
        else:
            return True

    def is_active(self):
        return self.active

    def is_ready(self):
        return self.ready

    def set_ready(self):
        self.ready = True

    def time_left(self):
        seconds = (self.end_time - datetime.datetime.now()).total_seconds()
        return seconds if seconds > 0 else 0
