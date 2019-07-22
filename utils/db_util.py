import sqlalchemy as db
from const import user, password, host, db_name

DATABASE_URI = 'mysql+mysqldb://{0}:{1}@{2}/{3}?charset=utf8'.format(user, password, host, db_name)
engine = db.create_engine(DATABASE_URI)
metadata = db.MetaData(engine)


def create_ticket(event_id, place):
    engine.execute("INSERT INTO tickets (event_id, place)"
                   "VALUES ({},{})".format(event_id, place))


def add_new_user_if_not_exist(msg):
    tg_user = msg.from_user

    res = engine.execute("INSERT IGNORE INTO users (tg_id, f_name, l_name) "
                         "VALUES ({}, '{}', '{}') ".format(tg_user.id, tg_user.first_name, tg_user.last_name))


def get_all_events():
    res = engine.execute("SELECT e.*, "
                         "  ("
                         "      SELECT t.id FROM tickets t "
                         "      WHERE t.event_id = e.id AND t.user_id IS NULL"
                         "      LIMIT 1"
                         "  ) AS is_tickets "
                         "FROM `events` e")
    return res.fetchall()


def get_booked(msg):
    res = engine.execute("SELECT e.name, t.id, t.place "
                         "FROM `events` e "
                         "LEFT JOIN tickets t ON (e.id=t.event_id) "
                         "LEFT JOIN users u ON (t.user_id=u.id) "
                         "WHERE u.tg_id={} "
                         "ORDER BY e.creation_date".format(msg.from_user.id))
    return res.fetchall()


def get_event(event_id):
    res = engine.execute("SELECT e.name, e.about, t.place, t.id "
                         "FROM `events` e "
                         "LEFT JOIN tickets t ON (e.id=t.event_id) "
                         "WHERE e.id={} AND t.user_id IS NULL".format(event_id))
    return res.fetchall()


def get_ticket_with_user(ticket_id, user_tg_id=None):
    if user_tg_id :
        q = "SELECT * " \
            "FROM tickets t " \
            "LEFT JOIN users u ON (t.user_id) " \
            "WHERE t.id={} AND u.tg_id={}".format(ticket_id, user_tg_id)
    else:
        q = "SELECT * " \
            "FROM tickets t " \
            "LEFT JOIN users u ON (t.user_id) " \
            "WHERE t.id={} AND u.tg_id IS NULL".format(ticket_id)

    res = engine.execute(q)
    return res.first()


def book(msg, ticket_id):
    ticket_with_user = get_ticket_with_user(ticket_id)

    if not ticket_with_user:
        return False
    res = engine.execute("UPDATE tickets t, users u "
                         "SET t.user_id=u.id "
                         "WHERE u.tg_id={} AND t.id={}".format(msg.from_user.id, ticket_id))
    return True


def del_book(msg, ticket_id):
    tg_id = msg.from_user.id

    ticket_with_user = get_ticket_with_user(ticket_id, tg_id)

    if not ticket_with_user or ticket_with_user.tg_id != tg_id:
        return False
    res = engine.execute("UPDATE tickets t "
                         "SET t.user_id=NULL "
                         "WHERE t.id={}".format(ticket_id))
    return True


def get_all_booked():
    res = engine.execute("SELECT e.name, CONCAT(u.f_name, ' ', u.l_name) AS user_name, t.place "
                         "FROM tickets t "
                         "JOIN `events` e ON (t.event_id=e.id) "
                         "JOIN users u ON (t.user_id=u.id) ")
    return res.fetchall()
