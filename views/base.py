from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
import settings
import logging
from classes.user import UsersClass
from classes.notes import NotesClass

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
	user = update.message.from_user
	logger.info("User %s init", user.id)

	user = UsersClass(user.id)
	if(user.dialog):
		data = user.dialog.data.split('|')
		step = data[0]
		data = data[1]
		return '{}_{}'.format(step, data)
	else:
		buttons = [
				InlineKeyboardButton("Тайминг", callback_data='100_1'),
		]
		keyboard = settings.constructor(buttons, settings.COUNT_ROW)
		reply_markup = InlineKeyboardMarkup(keyboard)
		update.message.reply_text(
			"Тайминг (напоминания, уведомления, сообщения)",
			reply_markup=reply_markup
		)
		return 'START'


def end(update, context):
	"""Returns `ConversationHandler.END`, which tells the
	ConversationHandler that the conversation is over"""
	query = update.callback_query
	query.answer()
	query.edit_message_text(
		text="See you next time!"
	)
	return ConversationHandler.END