from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

import const

bot = TeleBot(const.BOT_TOKEN)


def send_start_message(msg):
    tg_id = msg.from_user.id
    f_name = msg.from_user.first_name

    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    to_book = KeyboardButton('Забронювати')
    booked = KeyboardButton('Мої квитки')
    keyboard.add(to_book, booked)

    bot.send_message(tg_id, 'Привіт {}, дякую що приєднався до мене!\n'
                            'Я допоможу тобі забронювати квитки, '
                            'просто скористайся кнопками клавіатури...'.format(f_name), reply_markup=keyboard)


def send_events(msg, events):
    tg_id = msg.from_user.id

    text = '<b>Події</b>'
    for e in events:
        if e.is_tickets:
            text += '\n----------\n' \
                    '<b>Назва:</b> {}\n' \
                    '<b>Опис:</b> {}\n' \
                    '<b>Білети:</b> /ev_{}'.format(e.name, e.about, e.id)

    bot.send_message(tg_id, text, parse_mode='html')


def send_event(msg, event):
    tg_id = msg.from_user.id

    if event:
        text = '<b>Подія:</b> ' + event[0].name
        for t in event:
            text += '\n----------\n' \
                    '<b>Місце:</b> {}\n' \
                    '<b>Забронювати:</b> /book_{}'.format(t.place, t.id)
        bot.send_message(tg_id, text, parse_mode='html')


def send_booked(msg, booked):
    tg_id = msg.from_user.id

    text = '<b>Заброньовані</b>'
    for b in booked:
        text += '\n----------\n' \
                '<b>Назва:</b> {}\n' \
                '<b>Місце:</b> {}\n' \
                '<b>Видалити:</b> /del_{}'.format(b.name, b.place, b.id)

    bot.send_message(tg_id, text, parse_mode='html')


def send_is_booked(msg):
    tg_id = msg.from_user.id

    bot.send_message(tg_id, 'Супер, білет заброньовано.\n'
                            'Щоб переглянути список заброньованих натисніть кнопку \'Мої квитки\'.')


def send_is_not_booked(msg):
    tg_id = msg.from_user.id

    bot.send_message(tg_id, 'Помилка. Неможливо купити цей білет.')


def send_is_deleted(msg):
    tg_id = msg.from_user.id

    bot.send_message(tg_id, 'Бронь знято.\n'
                            'Перегляньте інші події натиснувши \'Забронювати\'.')


def send_is_not_deleted(msg):
    tg_id = msg.from_user.id

    bot.send_message(tg_id, 'Помилка. Неможливо зняти бронь з цього білету.')


def send_all_booked(msg, booked):
    tg_id = msg.from_user.id

    text = '<b>Заброньовано:</b>\n'
    for b in booked:
        text += '{} - {} - {}\n'.format(b.name, b.place, b.user_name)

    bot.send_message(tg_id, text, parse_mode='html')
