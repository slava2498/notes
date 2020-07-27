#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
import settings
from views import times, base, dialog
import inittable
import sender

def main():
    updater = Updater(settings.TOKEN, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', base.start)],
        states={
            'START': [
                        CallbackQueryHandler(times.start_over, pattern='^' + '100'),
            ],
            'TIMING': [
                        CallbackQueryHandler(times.one, pattern='^' + '100'),
                        CallbackQueryHandler(times.pagin, pattern='^' + '101'),
                        CallbackQueryHandler(times.settings_detail, pattern='^' + '103'),
                        CallbackQueryHandler(times.create, pattern='^' + '104'),
                        CallbackQueryHandler(times.delete, pattern='^' + '105'),

                        CallbackQueryHandler(times.mode_detail, pattern='^' + '106'),
                        CallbackQueryHandler(times.date_detail, pattern='^' + '107'),
                        CallbackQueryHandler(times.hour_detail, pattern='^' + '110'),
                        CallbackQueryHandler(times.minute_detail, pattern='^' + '111'),
                        CallbackQueryHandler(times.minute_add, pattern='^' + '112'),
                        CallbackQueryHandler(times.date_add, pattern='^' + '114'),
                        CallbackQueryHandler(times.date_delete, pattern='^' + '115'),

                        CallbackQueryHandler(times.settings_name, pattern='^' + '108'),
                        CallbackQueryHandler(times.settings_mode, pattern='^' + '109'),
            ],
            'DIALOG': [
                        MessageHandler(Filters.text, dialog.text),
                        CallbackQueryHandler(times.stop, pattern='^' + '777'),

                        CallbackQueryHandler(times.create, pattern='^' + '104'),
                        CallbackQueryHandler(times.delete, pattern='^' + '105'),

                        CallbackQueryHandler(times.mode_detail, pattern='^' + '106'),
                        CallbackQueryHandler(times.date_detail, pattern='^' + '107'),
                        CallbackQueryHandler(times.hour_detail, pattern='^' + '110'),
                        CallbackQueryHandler(times.minute_detail, pattern='^' + '111'),

                        CallbackQueryHandler(times.settings_name, pattern='^' + '108'),
                        CallbackQueryHandler(times.settings_mode, pattern='^' + '109'),
            ],
        },
        fallbacks=[CommandHandler('start', base.start)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.text, dialog.text))

    updater.job_queue.run_repeating(sender.main, interval=10, first=0)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()