# core structure of the bot
import telebot
from telebot import types
from mongoengine import *
from SearchEngine.SearchByName import *
from SearchEngine.SearchByYear import *
from SearchEngine.SearchByDirector import *
from SearchEngine.SearchByActor import *
from SearchEngine.RandomMovie import *
from SearchEngine.MostPopular import *
from SearchEngine.SearchByGenre import *


bot = telebot.TeleBot('1002991204:AAHnJ2q9kV1htX5iRREZpW0Vg_6xOFOOSao')
connect("cinebot_database")


class State(Document):
    user_id = StringField(required=True, unique=True)
    state = ListField()
    mode = StringField()


@bot.message_handler(commands=['help'])
def help_msg(msg):
    txt = '''
Данный бот создан независимой командой разработки Pythlings в рамках летней практики в МГТУ им. Н.Э.Баумана.\n\n
Он предназначен для решения задачи оптимизации времени поиска фильмов и сериалов.\n
/start - приветственное сообщение.
/go - начать поиск.
/restart - перезапустить поиск.
/back - вернуться к предыдущему шагу.
/help - получение справки.
'''
    bot.send_message(msg.from_user.id, text=txt)


@bot.message_handler(commands=['start'])

def welcome_msg(msg):
    try:
        user = State(user_id=str(msg.from_user.id))
        user.save()
    except:
        pass
    user_data = (State.objects(user_id=str(msg.chat.id)))[0]
    user_data.state = ['старт']
    user_data.save()
    bot.send_message(msg.from_user.id, text='Тебя приветствует Cinebot, мы поможем тебе отлично провести время за просмотром фильмов 🎥.\n\
Напиши /go и начнем искать!🔎', reply_markup = types.ReplyKeyboardRemove())

@bot.message_handler(commands=['back'])
def back(msg):
    try:
        user_data = (State.objects(user_id=str(msg.chat.id)))[0]
        if len(user_data.state) == 2:
            user_data.mode = ''
        user_data.state.pop()
        if user_data.state[-1] == 'старт': welcome_msg(msg)
        elif user_data.state[-1] == 'мод': go(msg)
        elif user_data.state[-1] == 'меню' and user_data.mode == 'фильм': mainmenu(msg)
        elif user_data.mode == 'фильм': mainmenu(msg)
        user_data.save()
    except:
        pass


@bot.message_handler(commands=['go', 'restart'])
@bot.message_handler(func=lambda msg: ((State.objects(user_id=str(msg.chat.id)))[0].state[-1] == 'старт'))
def go(msg):
    type_reply = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    movie = types.KeyboardButton(text="🎬 Фильм")
    series = types.KeyboardButton(text="📺 Сериал")
    type_reply.row(movie, series)
    bot.send_message(msg.chat.id, text="Что хочешь посмотреть, {}?".format(msg.chat.first_name),
                     reply_markup=type_reply)
    State.objects(user_id=str(msg.from_user.id)).update(state=['старт', 'мод'], mode='')





@bot.message_handler(func=lambda msg: ((State.objects(user_id=str(msg.chat.id)))[0].state[-1] == 'мод' and msg.text == "📺 Сериал"))
def serial(msg):
    user_data = (State.objects(user_id=str(msg.chat.id)))[0]
    user_data.mode = 'сериал'
    user_data.save()
    bot.send_message(msg.chat.id, text='К сожалению данный функционал пока недоступен :(',
                     reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(func=lambda msg: ((State.objects(user_id=str(msg.chat.id)))[0].state[-1] == 'мод' and msg.text == "🎬 Фильм"))
def mainmenu(msg):
    popular = types.KeyboardButton("Популярное🍿")
    random = types.KeyboardButton("Случайный фильм🎲")
    actor = types.KeyboardButton("Актер💃🏻")
    director = types.KeyboardButton("Режиссер📽")
    genre = types.KeyboardButton("Жанр🎬")
    name = types.KeyboardButton("Название фильма🎙")
    year = types.KeyboardButton("Год выпуска 📅 ")
    search_reply = types.ReplyKeyboardMarkup()
    search_reply.row(actor, director, genre)
    search_reply.row(year, random)
    search_reply.row(popular, name)
    bot.send_message(msg.chat.id, text="Выбирай критерий👇", reply_markup=search_reply)
    user_data = (State.objects(user_id=str(msg.chat.id)))[0]
    user_data.mode = 'фильм'
    user_data.state.append('меню')
    user_data.save()


@bot.message_handler(func=lambda msg: (State.objects(user_id=str(msg.chat.id)))[0].state[-1] == 'меню' and \
                                      (State.objects(user_id=str(msg.chat.id)))[0].mode == 'фильм')
def find_movie(msg):
    reply = types.ReplyKeyboardRemove()
    if msg.text == "Популярное🍿" or msg.text.lower() == 'популярное':
        user_data = (State.objects(user_id=str(msg.chat.id)))[0]
        user_data.state.append('популярное')
        user_data.save()
        bot.send_message(msg.chat.id, text='Напиши любимую цифру и немного погоди', reply_markup=reply)
    elif msg.text == "Случайный фильм🎲" or msg.text.lower() == 'случайный фильм':
        user_data = (State.objects(user_id=str(msg.chat.id)))[0]
        user_data.state.append('случайный фильм')
        user_data.save()
        bot.send_message(msg.chat.id, text='Напиши любимую цифру и немного погоди', reply_markup=reply)
    elif msg.text == "Актер💃🏻" or msg.text.lower() == 'актер':
        user_data = (State.objects(user_id=str(msg.chat.id)))[0]
        user_data.state.append('актер')
        user_data.save()
        bot.send_message(msg.chat.id, text='Напиши имя актера и погоди немного', reply_markup=reply)
    elif msg.text == "Режиссер📽" or msg.text.lower() == 'режиссер':
        user_data = (State.objects(user_id=str(msg.chat.id)))[0]
        user_data.state.append('режиссер')
        user_data.save()
        bot.send_message(msg.chat.id, text='Напиши имя режиссера и погоди немного', reply_markup=reply)
    elif msg.text == "Жанр🎬" or msg.text.lower() == 'жанр':
        user_data = (State.objects(user_id=str(msg.chat.id)))[0]
        user_data.state.append('жанр')
        user_data.save()
        bot.send_message(msg.chat.id, text='Напиши название жанра и погоди немного', reply_markup=reply)
    elif msg.text == "Название фильма🎙" or msg.text.lower() == 'название фильма':
        user_data = (State.objects(user_id=str(msg.chat.id)))[0]
        user_data.state.append('название фильма')
        user_data.save()
        bot.send_message(msg.chat.id, text='Напиши название фильма и немного погоди', reply_markup=reply)
    elif msg.text == "Год выпуска 📅" or msg.text.lower() == 'год выпуска':
        user_data = (State.objects(user_id=str(msg.chat.id)))[0]
        user_data.state.append('год выпуска')
        user_data.save()
        bot.send_message(msg.chat.id, text='Напиши год выпуска и немного погоди', reply_markup=reply)
    else:
        bot.send_message(msg.chat.id, text="Я тебя не понимаю", reply_markup=reply)


@bot.message_handler(func=lambda msg: (State.objects(user_id=str(msg.chat.id)))[0].state[-1] == 'популярное' and \
                                      (State.objects(user_id=str(msg.chat.id)))[0].mode == 'фильм')
def search_popular(msg):
    if top_five(msg, bot) == '-1':
        bot.send_message(msg.chat.id, text='К сожалению мне не удалось ничего найти')
    user_data = (State.objects(user_id=str(msg.chat.id)))[0]
    user_data.state.append('Нашел')
    user_data.save()
    bot.send_message(msg.chat.id, text='Введите команду /restart, чтобы подобрать что-нибудь новенькое.')


@bot.message_handler(func=lambda msg: (State.objects(user_id=str(msg.chat.id)))[0].state[-1] == 'случайный фильм' and \
                                      (State.objects(user_id=str(msg.chat.id)))[0].mode == 'фильм')
def search_random(msg):
    if get_random(msg, bot) == '-1':
        bot.send_message(msg.chat.id, text='К сожалению мне не удалось ничего найти')
    user_data = (State.objects(user_id=str(msg.chat.id)))[0]
    user_data.state.append('Нашел')
    user_data.save()
    bot.send_message(msg.chat.id, text='Введите команду /restart, чтобы подобрать что-нибудь новенькое.')


@bot.message_handler(func=lambda msg: (State.objects(user_id=str(msg.chat.id)))[0].state[-1] == 'актер' and \
                                      (State.objects(user_id=str(msg.chat.id)))[0].mode == 'фильм')
def search_actor(msg):
    if by_actor(msg.text, msg, bot) == '-1':
        bot.send_message(msg.chat.id, text='К сожалению мне не удалось ничего найти')
    user_data = (State.objects(user_id=str(msg.chat.id)))[0]
    user_data.state.append('Нашел')
    user_data.save()
    bot.send_message(msg.chat.id, text='Введите команду /restart, чтобы подобрать что-нибудь новенькое.')


@bot.message_handler(func=lambda msg: (State.objects(user_id=str(msg.chat.id)))[0].state[-1] == 'режиссер' and \
                                      (State.objects(user_id=str(msg.chat.id)))[0].mode == 'фильм')
def search_director(msg):
    if by_director(msg.text, msg, bot) == '-1':
        bot.send_message(msg.chat.id, text='К сожалению мне не удалось ничего найти')
    user_data = (State.objects(user_id=str(msg.chat.id)))[0]
    user_data.state.append('Нашел')
    user_data.save()
    bot.send_message(msg.chat.id, text='Введите команду /restart, чтобы подобрать что-нибудь новенькое.')


@bot.message_handler(func=lambda msg: (State.objects(user_id=str(msg.chat.id)))[0].state[-1] == 'жанр' and \
                                      (State.objects(user_id=str(msg.chat.id)))[0].mode == 'фильм')
def search_genre(msg):
    if by_genre(msg.text, msg, bot) == '-1':
        bot.send_message(msg.chat.id, text = 'К сожалению мне не удалось ничего найти')
    user_data = (State.objects(user_id=str(msg.chat.id)))[0]
    user_data.state.append('Нашел')
    user_data.save()
    bot.send_message(msg.chat.id, text = 'Введите команду /restart, чтобы подобрать что-нибудь новенькое.')


@bot.message_handler(func=lambda msg: (State.objects(user_id=str(msg.chat.id)))[0].state[-1] == 'название фильма' and \
                                      (State.objects(user_id=str(msg.chat.id)))[0].mode == 'фильм')
def search_name(msg):
    if by_name(msg.text, msg, bot) == '-1':
        bot.send_message(msg.chat.id, text = 'К сожалению мне не удалось ничего найти')
    user_data = (State.objects(user_id=str(msg.chat.id)))[0]
    user_data.state.append('Нашел')
    user_data.save()
    bot.send_message(msg.chat.id, text = 'Введите команду /restart, чтобы подобрать что-нибудь новенькое.')

@bot.message_handler(func=lambda msg: (State.objects(user_id=str(msg.chat.id)))[0].state[-1] == 'год выпуска' and \
                                      (State.objects(user_id=str(msg.chat.id)))[0].mode == 'фильм')
def search_year(msg):
    if by_year(msg.text, msg, bot) == '-1':
        bot.send_message(msg.chat.id, text='К сожалению мне не удалось ничего найти')
    user_data = (State.objects(user_id=str(msg.chat.id)))[0]
    user_data.state.append('Нашел')
    user_data.save()
    bot.send_message(msg.chat.id, text='Введите команду /restart, чтобы подобрать что-нибудь новенькое.')


bot.polling()
