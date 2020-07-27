import requests
import telebot
from models import *
from telebot import types
from datetime import datetime, timedelta, date
import os
import settings
import pytz
import inittable
from dateutil.relativedelta import relativedelta
import timestring
import telegram.ext

# bot = telebot.TeleBot(settings.TOKEN)
def main(context: telegram.ext.CallbackContext):
    now = datetime.now(pytz.timezone('Europe/Kiev'))
    today = now.today()
    day = today.weekday()

    hour = now.hour
    minute = now.minute

    print(day + 1, hour, minute)
    datesh = DateTimeScheduler.select().where(DateTimeScheduler.num_day == str(day + 1), DateTimeScheduler.hour == hour, DateTimeScheduler.minute == minute, DateTimeScheduler.send == False, DateTimeScheduler.end == False, DateTimeScheduler.state == True)

    for x in datesh:
        if(x.scheduler.mode == 'regularly'):
            state = True
            x.send = True
            x.time_send = now
            x.save()
        elif(x.scheduler.mode == 'onetime'):
            state = True
            x.end = True
            x.send = True
            x.time_send = now
            x.save()
        elif(x.scheduler.mode == 'week' and (x.time_send is None or now > datetime.fromisoformat(x.time_send) + relativedelta(weeks=1))):
            state = True
            x.send = True
            x.time_send = now
            x.save()
        elif(x.scheduler.mode == 'month' and (x.time_send is None or now > datetime.fromisoformat(x.time_send) + relativedelta(months=1))):
            state = True
            x.send = True
            x.time_send = now
            x.save()
        elif(x.scheduler.mode == 'quarter' and (x.time_send is None or now > datetime.fromisoformat(x.time_send) + relativedelta(months=6))):
            state = True
            x.send = True
            x.time_send = now
            x.save()

        if(state):
            sh = Scheduler.select().where(Scheduler.id == x.scheduler_id)
            context.bot.send_message(chat_id=sh[0].client.chat_id,
                             text=sh[0].body, 
                             parse_mode='Markdown')


        req = DateTimeScheduler.update(send=False).where(DateTimeScheduler.num_day != str(day), DateTimeScheduler.hour != hour, DateTimeScheduler.minute != minute, DateTimeScheduler.send == True, DateTimeScheduler.end == False)
        req.execute()