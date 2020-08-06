#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import Updater, MessageHandler, Filters
import settings
from views import dialog
import inittable
import sender
from views import times

def main():
    updater = Updater(settings.TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(settings.step_hendler)
    dp.add_handler(MessageHandler(Filters.regex('^⏰ Тайминг$'), times.start_over))
    dp.add_handler(MessageHandler(Filters.text, dialog.text))
    

    updater.job_queue.run_repeating(sender.main, interval=10, first=0)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()