from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
import settings
import logging
from models import *
from classes.user import UsersClass
from classes.notes import NotesClass

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
				notes = NotesClass(user.client)
				notes.create(update.message.text)
				notes.get({'page': 1, 'count': settings.COUNT_PAGE})
				if(notes.state):
					update.message.reply_text(
						text=notes.scheduler.body,
						reply_markup=notes.reply_markup
					)
					user.delete_dialog()
				else:
					user.create_dialog('TIMING|104')
					update.message.reply_text('Введите текст напоминания')
					return 'DIALOG'

			elif(action == '108'):
				id = data[2]
				notes = NotesClass(user.client)
				notes.update(type_up='body', id=id, data=update.message.text)
				notes.detail(id)
				update.message.reply_text(
					text=notes.scheduler.body,
					reply_markup=notes.reply_markup
				)
				user.delete_dialog()


		return '{}'.format(step)