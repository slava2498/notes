from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from views import times, base, dialog

constructor = lambda A, n: [A[i:i+n] for i in range(0, len(A), n)]
TOKEN = '1329404959:AAHmdiVNdSoAVqC2jOWvraevYDZkByb2GN0'
COUNT_ROW = 1
COUNT_PAGE = 1
MEDIA_TECH = 'AgACAgIAAxkBAAIEDV8oBWRrlh_xIlDwuFeGXF7XBPS7AAJNrzEb7U9ASQwYS1Ne9w7CgA8Fki4AAwEAAwIAA3gAA_2iBAABGgQ'

step_hendler = ConversationHandler(
    entry_points=[
        CommandHandler('start', base.start),
        MessageHandler(Filters.regex('^⏰ Тайминг$'), times.start_over),
    ],
    states={
        'START': [
                    MessageHandler(Filters.regex('^⏰ Тайминг$'), times.start_over),
        ],
        'TIMING': [
                    CallbackQueryHandler(times.one, pattern='^' + '100'),
                    CallbackQueryHandler(times.pagin, pattern='^' + '101'),
                    CallbackQueryHandler(times.create, pattern='^' + '104'),
                    CallbackQueryHandler(times.delete, pattern='^' + '105'),

                    CallbackQueryHandler(times.settings_detail, pattern='^' + '103'),
                    CallbackQueryHandler(times.mode_detail, pattern='^' + '106'),
                    CallbackQueryHandler(times.date_detail, pattern='^' + '107'),
                    CallbackQueryHandler(times.hour_detail, pattern='^' + '110'),
                    CallbackQueryHandler(times.minute_detail, pattern='^' + '111'),

                    CallbackQueryHandler(times.date_detail, pattern='^' + '116'),
                    CallbackQueryHandler(times.hour_detail, pattern='^' + '117'),

                    CallbackQueryHandler(times.minute_add, pattern='^' + '112'),
                    CallbackQueryHandler(times.date_add, pattern='^' + '114'),
                    CallbackQueryHandler(times.date_delete, pattern='^' + '115'),

                    CallbackQueryHandler(times.settings_name, pattern='^' + '108'),
                    CallbackQueryHandler(times.settings_mode, pattern='^' + '109'),
                    CallbackQueryHandler(times.settings_period, pattern='^' + '189'),
                    CallbackQueryHandler(times.period_detail, pattern='^' + '199'),

                    CallbackQueryHandler(times.important, pattern='^' + '200'),
                    CallbackQueryHandler(times.importantpagin, pattern='^' + '201'),
                    CallbackQueryHandler(times.importantcreate, pattern='^' + '204'),
                    CallbackQueryHandler(times.importantdelete, pattern='^' + '205'),

                    CallbackQueryHandler(times.importantdetail, pattern='^' + '203'),
                    CallbackQueryHandler(times.importantmode, pattern='^' + '206'),
                    CallbackQueryHandler(times.settings_mode_important, pattern='^' + '209'),
                    CallbackQueryHandler(times.settings_importantdate, pattern='^' + '207'),
                    CallbackQueryHandler(times.hour_importantdetail, pattern='^' + '210'),
                    CallbackQueryHandler(times.settings_importantname, pattern='^' + '208'),

                    CallbackQueryHandler(times.minute_importantdetail, pattern='^' + '211'),
                    CallbackQueryHandler(times.minute_importantadd, pattern='^' + '212'),

                    CallbackQueryHandler(times.start_over, pattern='^' + '888'),
                    CallbackQueryHandler(base.end, pattern='^' + '999'),
                    CallbackQueryHandler(times.stopnoti, pattern='^' + '555'),
                    CallbackQueryHandler(times.stopimpo, pattern='^' + '556'),
        ],
        'DIALOG': [
                    MessageHandler(Filters.text, dialog.text),
                    MessageHandler(Filters.photo, dialog.get_image),

                    CallbackQueryHandler(times.stop, pattern='^' + '777'),

                    CallbackQueryHandler(times.one, pattern='^' + '100'),
                    CallbackQueryHandler(times.pagin, pattern='^' + '101'),
                    CallbackQueryHandler(times.create, pattern='^' + '104'),
                    CallbackQueryHandler(times.delete, pattern='^' + '105'),

                    CallbackQueryHandler(times.settings_detail, pattern='^' + '103'),
                    CallbackQueryHandler(times.mode_detail, pattern='^' + '106'),
                    CallbackQueryHandler(times.date_detail, pattern='^' + '107'),
                    CallbackQueryHandler(times.hour_detail, pattern='^' + '110'),
                    CallbackQueryHandler(times.minute_detail, pattern='^' + '111'),

                    CallbackQueryHandler(times.date_detail, pattern='^' + '116'),
                    CallbackQueryHandler(times.hour_detail, pattern='^' + '117'),

                    CallbackQueryHandler(times.minute_add, pattern='^' + '112'),
                    CallbackQueryHandler(times.date_add, pattern='^' + '114'),
                    CallbackQueryHandler(times.date_delete, pattern='^' + '115'),

                    CallbackQueryHandler(times.settings_name, pattern='^' + '108'),
                    CallbackQueryHandler(times.settings_mode, pattern='^' + '109'),
                    CallbackQueryHandler(times.settings_period, pattern='^' + '189'),
                    CallbackQueryHandler(times.period_detail, pattern='^' + '199'),

                    CallbackQueryHandler(times.important, pattern='^' + '200'),
                    CallbackQueryHandler(times.importantpagin, pattern='^' + '201'),
                    CallbackQueryHandler(times.importantcreate, pattern='^' + '204'),
                    CallbackQueryHandler(times.importantdelete, pattern='^' + '205'),

                    CallbackQueryHandler(times.importantdetail, pattern='^' + '203'),
                    CallbackQueryHandler(times.importantmode, pattern='^' + '206'),
                    CallbackQueryHandler(times.settings_mode_important, pattern='^' + '209'),
                    CallbackQueryHandler(times.settings_importantdate, pattern='^' + '207'),
                    CallbackQueryHandler(times.hour_importantdetail, pattern='^' + '210'),
                    CallbackQueryHandler(times.settings_importantname, pattern='^' + '208'),

                    CallbackQueryHandler(times.minute_importantdetail, pattern='^' + '211'),
                    CallbackQueryHandler(times.minute_importantadd, pattern='^' + '212'),

                    CallbackQueryHandler(times.start_over, pattern='^' + '888'),
                    CallbackQueryHandler(base.end, pattern='^' + '999'),
                    CallbackQueryHandler(times.stopnoti, pattern='^' + '555'),
                    CallbackQueryHandler(times.stopimpo, pattern='^' + '556'),

        ],
    },
    fallbacks=[CommandHandler('start', base.start)]
)