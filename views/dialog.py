from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputMediaPhoto
import settings
import logging
import calendar
import datetime
from models import *
from classes.user import UsersClass
from classes.notes import NotesClass
from classes.important import ImportantClass

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)

def text(update, context):
	query = update.message
	print(query)
	user = UsersClass(query.from_user.id)
	if(user.dialog):
		data = user.dialog.data.split('|')
		print(data)

		step = data[0]
		action = data[1]

		if(step == 'TIMING'):
			if(action == '104'):
				notes = NotesClass(user.client, None)
				notes.create(update.message.text)
				notes.get({'page': 1, 'count': settings.COUNT_PAGE})
				if(notes.state):
					context.bot.sendPhoto(chat_id=query.chat.id, photo=notes.scheduler.file_patch, caption=notes.scheduler.body, reply_markup=notes.reply_markup)
					user.delete_dialog()
				else:
					user.create_dialog('TIMING|104')
					update.message.reply_text('Введите текст напоминания')
					return 'DIALOG'

			elif(action == '108'):
				id = data[2]
				notes = NotesClass(user.client, None)
				notes.update(type_up='body', id=id, data=update.message.text)
				notes.detail(id)
				
				context.bot.sendPhoto(chat_id=query.chat.id, photo=notes.scheduler.file_patch, caption=notes.scheduler.body, reply_markup=notes.reply_markup)
				user.delete_dialog()

			elif(action == '200'):
				notes = ImportantClass(user.client, None)
				notes.create(update.message.text)
				notes.get({'page': 1, 'count': settings.COUNT_PAGE})
				if(notes.state):
					# context.bot.sendPhoto(chat_id=query.chat.id, photo=notes.important.file_patch, caption=notes.important.body, reply_markup=notes.reply_markup)
					user = UsersClass(query.from_user.id)
					notes = ImportantClass(user.client, notes.important.id)
					user.delete_dialog()
					user.create_dialog('TIMING|209|{}'.format(notes.important.id))

					# context.bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)
					context.bot.send_message(chat_id=query.chat.id, text='Введите дату в формате дд.мм', parse_mode='Markdown')
					return 'DIALOG'
				else:
					user.create_dialog('TIMING|200')
					update.message.reply_text('Введите текст напоминания')
					return 'DIALOG'
				
				# context.bot.sendPhoto(chat_id=query.chat.id, photo=settings.MEDIA_TECH, caption=notes.important.body, reply_markup=notes.reply_markup)
				# user.delete_dialog()

			elif(action == '208'):
				id = data[2]
				notes = ImportantClass(user.client, None)
				notes.update(type_up='body', id=id, data=update.message.text)
				notes.detail(id)
				
				context.bot.sendPhoto(chat_id=query.chat.id, photo=notes.important.file_patch, caption=notes.important.body, reply_markup=notes.reply_markup)
				user.delete_dialog()

			elif(action == '209'):
				date = update.message.text.split('.')
				if(len(date) != 2):
					context.bot.send_message(chat_id=query.chat.id, text='Введите дату в формате дд.мм', parse_mode='Markdown')
					return '{}'.format(step)

				if(date[0][0] == '0'):
					day = date[0][1]
				else:
					day = date[0]

				if(date[1][0] == '0'):
					month = date[1][1]
				else:
					month = date[1]

				if not (1 <= int(day) <= 31):
					context.bot.send_message(chat_id=query.chat.id, text='Введите дату в формате дд.мм', parse_mode='Markdown')
					return '{}'.format(step)

				if not (1 <= int(month) <= 12):
					context.bot.send_message(chat_id=query.chat.id, text='Введите дату в формате дд.мм', parse_mode='Markdown')
					return '{}'.format(step)

				now = datetime.datetime.now()
				month_day = calendar.monthrange(now.year, 1)[1]

				if (int(day) > month_day):
					context.bot.send_message(chat_id=query.chat.id, text='В данном месяце количество дней = {}'.format(month_day), parse_mode='Markdown')
					return '{}'.format(step)

				id = data[2]
				notes = ImportantClass(user.client, None)
				notes.update(type_up='date', id=id, data=[day, month])
				notes.detail(id)
				
				if(notes.important.hour == None or notes.important.minute == None):
					buttons = []
					for x in range(1, 24):
						prefix = ''
						if(notes.important.hour == x):
							prefix = '✅'

						buttons.append(InlineKeyboardButton('{}{}'.format(prefix, x), callback_data='211_{}_{}'.format(notes.important.id, x)))

					keyboard = settings.constructor(buttons, 4)
					reply_markup = InlineKeyboardMarkup(keyboard)

					context.bot.sendPhoto(chat_id=query.chat.id, photo=notes.important.file_patch, caption='Выберите час', reply_markup=reply_markup)
					user.delete_dialog()
					return 'DIALOG'

				context.bot.sendPhoto(chat_id=query.chat.id, photo=notes.important.file_patch, caption=notes.important.body, reply_markup=notes.reply_markup)
				user.delete_dialog()

		return '{}'.format(step)

def get_image(update, context):
	"""Show new choice of buttons"""
	query = update.message
	user = UsersClass(query.from_user.id)
	if(user.dialog):
		data = user.dialog.data.split('|')
		print(data)

		step = data[0]
		action = data[1]

		if(step == 'TIMING'):
			if(action == '104'):
				notes = NotesClass(user.client, None)
				print(68, update.message.photo[-1].file_id)
				notes.create(update.message.text, update.message.photo[-1].file_id)

				user.create_dialog('TIMING|104')
				update.message.reply_text('Введите текст напоминания')

				user.delete_dialog()

			if(action == '200'):
				notes = ImportantClass(user.client, None)
				print(68, update.message.photo[-1].file_id)
				notes.create(update.message.text, update.message.photo[-1].file_id)

				user.create_dialog('TIMING|200')
				update.message.reply_text('Введите текст напоминания')

				user.delete_dialog()

	return 'DIALOG'