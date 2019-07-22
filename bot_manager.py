from utils.bot_util import bot
import utils.bot_util as front
import utils.db_util as back


@bot.message_handler(commands=['start'])
def start_command_handler(msg):
    back.add_new_user_if_not_exist(msg)
    front.send_start_message(msg)


@bot.message_handler(regexp=r'^Забронювати$')
def to_book_handler(msg):
    events = back.get_all_events()
    front.send_events(msg, events)


@bot.message_handler(regexp=r'^Мої квитки$')
def booked_handler(msg):
    booked = back.get_booked(msg)
    front.send_booked(msg, booked)


@bot.message_handler(regexp=r'^/ev_\d+$')
def ev_command_handler(msg):
    event_id = int(msg.text[len('/ev_'):])

    event = back.get_event(event_id)
    front.send_event(msg, event)


@bot.message_handler(regexp=r'^/book_\d+$')
def book_command_handler(msg):
    ticket_id = int(msg.text[len('/book_'):])

    if back.book(msg, ticket_id):
        front.send_is_booked(msg)
    else:
        front.send_is_not_booked(msg)


@bot.message_handler(regexp=r'^/del_\d+$')
def del_command_handler(msg):
    ticket_id = int(msg.text[len('/del_'):])

    if back.del_book(msg, ticket_id):
        front.send_is_deleted(msg)
    else:
        front.send_is_not_deleted(msg)


@bot.message_handler(commands=['show_booked'])
def show_booked_handler(msg):
    booked = back.get_all_booked()
    front.send_all_booked(msg, booked)


bot.polling()
