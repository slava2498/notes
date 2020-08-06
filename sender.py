import requests
from models import *
from datetime import datetime, timedelta, date
import os
import settings
import pytz
import inittable
from dateutil.relativedelta import relativedelta
import timestring
import telegram.ext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# bot = telebot.TeleBot(settings.TOKEN)
def main(context: telegram.ext.CallbackContext):
    now = datetime.now(pytz.timezone('Europe/Kiev'))
    today = now.today()
    day = today.weekday()

    hour = now.hour
    minute = now.minute
    num_days = now.day
    month = now.month
    year = now.year

    print(year, month, num_days, day + 1, hour, minute)
    datesh = DateTimeScheduler.select().where(DateTimeScheduler.num_day == str(day + 1), DateTimeScheduler.hour == hour, DateTimeScheduler.minute == minute, DateTimeScheduler.send == False, DateTimeScheduler.end == False, DateTimeScheduler.state == True)
    important = Important.select().where(Important.month == month, Important.day == num_days, Important.hour == hour, Important.minute == minute, Important.send == False, Important.end == False)

    for x in datesh:
        state = False
        if(x.scheduler.mode == 'onetime'):
            state = True
            x.end = True

        if(x.scheduler.period == 'week' and (x.time_send is None or now > datetime.fromisoformat(x.time_send) + relativedelta(weeks=1))):
            state = True
            x.send = True
            x.time_send = now
            x.save()
        elif(x.scheduler.period == '2week' and (x.time_send is None or now > datetime.fromisoformat(x.time_send) + relativedelta(weeks=2))):
            state = True
            x.send = True
            x.time_send = now
            x.save()
        elif(x.scheduler.period == 'month' and (x.time_send is None or now > datetime.fromisoformat(x.time_send) + relativedelta(months=1))):
            state = True
            x.send = True
            x.time_send = now
            x.save()

        if(state):
            sh = Scheduler.select().where(Scheduler.id == x.scheduler_id)
            buttons = [
                InlineKeyboardButton("Больше не напоминать ❌", callback_data='555_{}'.format(sh.id)),
            ]
            keyboard = settings.constructor(buttons, settings.COUNT_ROW)
            reply_markup = InlineKeyboardMarkup(keyboard)
            if(sh[0].file_patch != settings.MEDIA_TECH):
                context.bot.sendPhoto(chat_id=sh[0].client.chat_id, photo=sh[0].file_patch, caption=sh[0].body, reply_markup=reply_markup, parse_mode='Markdown')
            else:
                context.bot.send_message(chat_id=sh[0].client.chat_id,
                                        text=sh[0].body, 
                                        parse_mode='Markdown',
                                        reply_markup=reply_markup,)


        req = DateTimeScheduler.update(send=False).where(DateTimeScheduler.num_day != str(day), DateTimeScheduler.hour != hour, DateTimeScheduler.minute != minute, DateTimeScheduler.send == True, DateTimeScheduler.end == False)
        req.execute()

    for x in important:
        state = False
        if(x.mode == 'onetime'):
            state = True
            x.end = True

        if(x.time_send is None or now > datetime.fromisoformat(x.time_send) + relativedelta(year=1)):
            state = True
            x.send = True
            x.time_send = now
            x.save()

        if(state):
            buttons = [
                InlineKeyboardButton("Больше не напоминать ❌", callback_data='556_{}'.format(x.id)),
            ]
            keyboard = settings.constructor(buttons, settings.COUNT_ROW)
            reply_markup = InlineKeyboardMarkup(keyboard)
            if(x.file_patch != settings.MEDIA_TECH):
                context.bot.sendPhoto(chat_id=x.client.chat_id, photo=x.file_patch, caption=x.body, reply_markup=reply_markup, parse_mode='Markdown')
            else:
                context.bot.send_message(chat_id=x.client.chat_id,
                                        text=x.body, 
                                        parse_mode='Markdown',
                                        reply_markup=reply_markup,)