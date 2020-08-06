from peewee import *
import datetime
import settings

sqlite_db = SqliteDatabase('notes.db', pragmas={'journal_mode': 'wal'})

MEDIA_TECH = 'AgACAgIAAxkBAAIEDV8oBWRrlh_xIlDwuFeGXF7XBPS7AAJNrzEb7U9ASQwYS1Ne9w7CgA8Fki4AAwEAAwIAA3gAA_2iBAABGgQ'

MODE = {
    'regularly': "Регулярно",
    'onetime': "Единоразово",
}

PERIOD = {
    'week': "Неделя",
    '2week': "2 Недели",
    'month': "Месяц",
}

DAYS = {
    1: "Понедельник",
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница",
    6: "Суббота",
    7: "Воскресенье",
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


MODE_IMPORTANT = {
    'regularly': "Ежегодно",
    'onetime': "Разово",
}

class BaseModel(Model):
    class Meta:
        database = sqlite_db

class Clients(BaseModel):
    chat_id = CharField()

class Scheduler(BaseModel):
    client = ForeignKeyField(Clients, backref='client')
    body = TextField(null=True)
    file_patch = CharField(default=MEDIA_TECH)

    mode = CharField(choices=MODE, null=True)
    period = CharField(choices=PERIOD, null=True)
    created_date = DateTimeField(default=datetime.datetime.now)

class Important(BaseModel):
    client = ForeignKeyField(Clients, backref='client')
    body = TextField(null=True)
    file_patch = CharField(default=MEDIA_TECH)

    mode = CharField(choices=MODE_IMPORTANT, null=True)
    hour = IntegerField(null=True)
    minute = IntegerField(null=True)

    month = IntegerField(null=True)
    day = IntegerField(null=True)
    created_date = DateTimeField(default=datetime.datetime.now)

    time_send = DateTimeField(null=True)
    send = BooleanField(default=False)
    end = BooleanField(default=False)

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