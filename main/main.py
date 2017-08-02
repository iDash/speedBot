import copy
import datetime

import constants
import engine
import telebot

commands = {  # command description used in the "help" command
    'start': 'Правила',
    'run': 'Подготова играы агентом',
    'go': 'Старт игрока',
    'time': "Оставшееся время"
}

bot = telebot.TeleBot(constants.TOKEN)
game = engine.Game()
codes = copy.copy(constants.CODES)


# only used for console output now
def log_listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print("{0} Message from {1} {2} (id={3}): {4}".format(datetime.datetime.now(), m.from_user.first_name,
                                                                  m.from_user.last_name, str(m.from_user.id), m.text))


bot.set_update_listener(log_listener)  # register listener


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    bot.send_message(m.chat.id, constants.RULES)


# handle the "/run" command
@bot.message_handler(commands=['run'])
def command_run(m):
    global game
    global codes
    cid = m.from_user.id
    if cid in constants.ADMINS:
        if game.is_active():
            bot.send_message(m.chat.id, "Игра была уже запущенна. Осталось {0} секунд!".format(game.time_left()))
        else:
            codes = copy.copy(constants.CODES)
            game = engine.Game()
            game.set_ready()
            bot.send_message(m.chat.id, "Все готово! Let's /go!")
    else:
        bot.send_message(m.chat.id, constants.NO_PERMISSION)


# handle the "/go" command
@bot.message_handler(commands=['go'])
def command_run(m):
    global game
    if game.is_ready():
        game.start(m.from_user.id)
        bot.send_message(m.chat.id, "Беги {0}! Осталось {1} секунд!".format(m.from_user.first_name, game.time_left()))


# handle the "/time" command
@bot.message_handler(commands=['time'])
def command_time(m):
    global game
    if game.is_active():
        bot.send_message(m.chat.id, "Осталось {0} секунд".format(game.time_left()))
    else:
        bot.send_message(m.chat.id, "Игра завершена")


# handle the "/finish" command
@bot.message_handler(commands=['finish'])
def command_finish(m):
    global game
    if not game.check() and game.same_player(m.from_user.id):
        bot.send_message(m.chat.id,
                         "Взято кодов: {0}. Бонус: {1} секунд".format(game.level, engine.EN_BONUS_TIME[game.level]))
        if game.level > 0:
            bot.send_message(m.chat.id, "Код для закрытия бонуса в движке: {0}".format(engine.EN_CODE[game.level]))
            bot.send_message(constants.ADMINS[0],
                             "Выслан код {0}: {1} {2}".format(engine.EN_CODE[game.level], m.from_user.first_name,
                                                              m.from_user.last_name))


# handle right answers
@bot.message_handler(func=lambda message: message.text.lower() in codes)
def command_right(m):
    global game
    global codes
    if game.same_player(m.from_user.id):
        if game.is_active():
            if game.check():
                game.level_up()
                codes.remove(m.text.lower())
                bot.send_message(m.chat.id, "+")
                bot.send_message(m.chat.id, "Осталось {0} секунд".format(game.time_left()))
                if not codes:
                    bot.send_message(m.chat.id, "Поздравляю! Все коды взяты. Жми /finish как /time выйдет")
            else:
                bot.send_message(m.chat.id, "Время вышло.")
                command_finish(m)
        else:
            bot.send_message(m.chat.id, "Игра завершена")


# handle right answers
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    global game
    if game.is_active():
        bot.send_message(m.chat.id, "-")
        bot.send_message(m.chat.id, "Осталось {0} секунд".format(game.time_left()))


while True:
    try:
        print("Server up and running")
        bot.send_message(constants.ADMINS[0], "Server up and running")
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print("Exception has appeared\n" + str(e))
        bot.send_message(constants.ADMINS[0], "Произошла ошибка")
