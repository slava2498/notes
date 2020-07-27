from peewee import *
import datetime

sqlite_db = SqliteDatabase('notes.db', pragmas={'journal_mode': 'wal'})

MODE = {
    'regularly': "Регулярно",
    'onetime': "Единоразово",
    'week': "Неделя",
    'month': "Месяц",
    'quarter': "Квартал",
}

DAYS = {
    1: "Пн",
    2: "Вт",
    3: "Ср",
    4: "Чт",
    5: "Пт",
    6: "Сб",
    7: "Вс",
}

HOUR = {
    1: "час",
    2: "часа",
    3: "часа",
    4: "часа",
    5: "часов",
    6: "часов",
    7: "часов",
    8: "часов",
    9: "часов",
    10: "часов",
    11: "часов",
    12: "часов",
    13: "часов",
    14: "часов",
    15: "часов",
    16: "часов",
    17: "часов",
    18: "часов",
    19: "часов",
    20: "часов",
    21: "час",
    22: "часа",
    23: "часа",
    24: "часа",
}
class BaseModel(Model):
    class Meta:
        database = sqlite_db

class Clients(BaseModel):
    chat_id = CharField()

class Scheduler(BaseModel):
    client = ForeignKeyField(Clients, backref='client')
    body = TextField()
    mode = CharField(choices=MODE, null=True)
    created_date = DateTimeField(default=datetime.datetime.now)

class DateTimeScheduler(BaseModel):
    scheduler = ForeignKeyField(Scheduler, backref='scheduler')
    num_day = CharField(choices=DAYS, null=True)
    hour = IntegerField(null=True)
    minute = IntegerField(null=True)
    state = BooleanField(default=False)

    time_send = DateTimeField(null=True)
    send = BooleanField(default=False)
    end = BooleanField(default=False)

class DialogControll(BaseModel):
	client = ForeignKeyField(Clients)
	data = TextField()