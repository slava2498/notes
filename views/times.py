from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputMediaPhoto
import settings
import logging
from models import *
from classes.user import UsersClass
from classes.notes import NotesClass
from classes.important import ImportantClass

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)

def start_over(update, context):
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
			InlineKeyboardButton("📝 Планировщик", callback_data='100'),
			InlineKeyboardButton("⚠️ Важные даты", callback_data='200'),
		]
		keyboard = settings.constructor(buttons, settings.COUNT_ROW)
		reply_markup = InlineKeyboardMarkup(keyboard)
		update.message.reply_text(
			text="Это ваш персональный планировщик дел на день, неделю, месяц и квартал",
			reply_markup=reply_markup
		)
		return 'TIMING'


def one(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client, None)
	if('_' in query.data):
		notes.get({'page': 1, 'count': settings.COUNT_PAGE, 'note_id': query.data.split('_')[1]})
	else:
		notes.get({'page': 1, 'count': settings.COUNT_PAGE})

	if(notes.state):
		if(notes.scheduler.file_patch):
			# context.bot.deleteMessage(chat_id=query.message.chat.id, message_id=update.message.message_id)
			context.bot.sendPhoto(chat_id=query.message.chat.id, photo=notes.scheduler.file_patch, caption=notes.scheduler.body, reply_markup=notes.reply_markup, parse_mode='Markdown')
		else:
			query.edit_message_text(
				text=notes.scheduler.body,
				reply_markup=notes.reply_markup,
				parse_mode='Markdown'
			)
		return 'TIMING'
	else:
		user.create_dialog('TIMING|104')

		buttons = [
				InlineKeyboardButton("Отменить ❌", callback_data='777'),
		]
		keyboard = settings.constructor(buttons, settings.COUNT_ROW)
		reply_markup = InlineKeyboardMarkup(keyboard)
		query.edit_message_text(
			'Введите текст напоминания или отправьте картинку',
			reply_markup=reply_markup,
			parse_mode='Markdown'
		)
		return 'DIALOG'

def pagin(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	print(data)
	page = int(data[1])

	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client, None)
	notes.get({'page': page, 'count': settings.COUNT_PAGE})
	if(notes.state):
		context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=notes.reply_markup, media=InputMediaPhoto(media=notes.scheduler.file_patch, caption=notes.scheduler.body, parse_mode='Markdown'))
		return 'TIMING'
	else:
		user.create_dialog('TIMING|104')
		context.bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)
		context.bot.send_message(chat_id=query.message.chat.id, text='Введите текст напоминания или отправьте картинку', parse_mode='Markdown')
		return 'DIALOG'

def create(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	user = UsersClass(query.from_user.id)
	user.create_dialog('TIMING|104')
	context.bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)
	context.bot.send_message(chat_id=query.message.chat.id, text='Введите текст напоминания или отправьте картинку', parse_mode='Markdown')
	return 'DIALOG'

def delete(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client, None)
	notes.delete(id)
	notes.get({'page': 1, 'count': settings.COUNT_PAGE})

	if(notes.state):
		context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=notes.reply_markup, media=InputMediaPhoto(media=notes.scheduler.file_patch, caption=notes.scheduler.body, parse_mode='Markdown'))
		return 'TIMING'
	else:
		buttons = [
			InlineKeyboardButton("📝 Планировщик", callback_data='100'),
			InlineKeyboardButton("⚠️ Важные даты", callback_data='200'),
		]
		keyboard = settings.constructor(buttons, settings.COUNT_ROW)
		reply_markup = InlineKeyboardMarkup(keyboard)
		
		context.bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)
		context.bot.send_message(chat_id=query.message.chat.id, text="Это ваш персональный планировщик дел на день, неделю, месяц и квартал", reply_markup=reply_markup, parse_mode='Markdown')
	return 'TIMING'

def stop(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	user = UsersClass(query.from_user.id)
	user.delete_dialog()
	query.edit_message_text(
		text="Действие отменено",
		parse_mode='Markdown'
	)
	return 'TIMING'

def settings_detail(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client, id)
	notes.detail(id)

	context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=notes.reply_markup, media=InputMediaPhoto(media=notes.scheduler.file_patch, caption=notes.scheduler.body), parse_mode='Markdown')
	return 'TIMING'

def mode_detail(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client, id)

	buttons = []
	for x in MODE:
		buttons.append(InlineKeyboardButton(MODE[x], callback_data='109_{}_{}'.format(id, x)))
	keyboard = settings.constructor(buttons, settings.COUNT_ROW)
	reply_markup = InlineKeyboardMarkup(keyboard)

	context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup, media=InputMediaPhoto(media=notes.scheduler.file_patch, caption='Выберите режим работы'), parse_mode='Markdown')
	return 'TIMING'

def period_detail(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client, id)

	buttons = []
	for x in PERIOD:
		buttons.append(InlineKeyboardButton(PERIOD[x], callback_data='189_{}_{}'.format(id, x)))
	keyboard = settings.constructor(buttons, settings.COUNT_ROW)
	reply_markup = InlineKeyboardMarkup(keyboard)

	context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup, media=InputMediaPhoto(media=notes.scheduler.file_patch, caption='Выберите период работы'), parse_mode='Markdown')
	return 'TIMING'

def settings_period(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	period = data[2]
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client, id)
	notes.update('period', id, period)
	notes.detail(id)

	context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=notes.reply_markup, media=InputMediaPhoto(media=notes.scheduler.file_patch, caption=notes.scheduler.body), parse_mode='Markdown')
	return 'TIMING'

def date_detail(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client, id)

	req = DateTimeScheduler.delete().where(DateTimeScheduler.state == False)
	req.execute()

	print(228, 'edit' in str(data))
	postfix = ''
	if('edit' in str(data)):
		postfix = 'edit_{}'.format(query.data.split('edit_')[1])
		dateTimeScheduler = DateTimeScheduler.get(DateTimeScheduler.id == query.data.split('edit_')[1])
		scheduler = dateTimeScheduler.scheduler
	else:
		scheduler = Scheduler.get(Scheduler.id == id)
		len_sh = DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id).count()
		print(len_sh,id)
		if(len_sh < 7):
			DateTimeScheduler.create(scheduler=scheduler)
		else:
			# context.bot.answer_callback_query(callback_query_id=update.callback_query.id, text='Ограничение: 7 напоминаний на заметку', show_alert=True)
			context.bot.send_message(chat_id=query.message.chat_id, text='Ограничение: 7 напоминаний на заметку')
			return 'TIMING'

	buttons = []
	for x in DAYS:
		buttons.append(InlineKeyboardButton(DAYS[x], callback_data='110_{}_{}_in_{}'.format(id, x, postfix)))
	keyboard = settings.constructor(buttons, settings.COUNT_ROW)
	reply_markup = InlineKeyboardMarkup(keyboard)
	reply_markup.inline_keyboard.append([InlineKeyboardButton("↩️ Назад", callback_data='103_{}'.format(id))])

	context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup, media=InputMediaPhoto(media=notes.scheduler.file_patch, caption='Выберите день недели'), parse_mode='Markdown')
	return 'TIMING'

def hour_detail(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	day = data[2]
	call = data[3]
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client, id)

	print('in' in str(data))
	print('edit' in str(data))
	print('edittime' in str(data))
	if('in' in str(data)):
		if('edit' in str(data)):
			id_date = query.data.split('edit_')[1]
			datesh = DateTimeScheduler.select().where(DateTimeScheduler.id == id_date)
		else:
			datesh = DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id, DateTimeScheduler.state == False)
		if(datesh and not 'edittime' in str(data)):
			datesh = datesh[0]
			datesh.num_day = int(day)
			datesh.save()

	buttons = []
	if('edit' in str(data)):
		if('edittime' in str(data)):
			id_date = query.data.split('edittime_')[1]
		else:
			id_date = query.data.split('edit_')[1]
		datesh = DateTimeScheduler.select().where(DateTimeScheduler.id == id_date)
	else:
		datesh = DateTimeScheduler.select().where(DateTimeScheduler.scheduler_id == id)

	postfix = ''
	if('edit' in str(data)):
		postfix = 'edit_{}'.format(id_date)
	for x in range(1, 24):
		prefix = ''
		for y in datesh:
			if(y.hour == x and day == y.num_day):
				prefix = '✅'


		buttons.append(InlineKeyboardButton('{}{}'.format(prefix, x), callback_data='111_{}_{}_{}_{}'.format(id, day, x, postfix)))

	keyboard = settings.constructor(buttons, 4)
	reply_markup = InlineKeyboardMarkup(keyboard)

	if('edit' not in str(data) and DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id, DateTimeScheduler.num_day != None, DateTimeScheduler.hour != None, DateTimeScheduler.minute != None, DateTimeScheduler.state == False)):
		reply_markup.inline_keyboard.append([InlineKeyboardButton("Готово", callback_data='114_{}'.format(id))])
	
	reply_markup.inline_keyboard.append([InlineKeyboardButton("↩️ Назад", callback_data='103_{}'.format(id))])
	context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup, media=InputMediaPhoto(media=notes.scheduler.file_patch, caption='День недели: *{}*\nВыберите час'.format(DAYS[int(day)]), parse_mode='Markdown'))
	return 'TIMING'

def minute_detail(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	day = data[2]
	hour = data[3]
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client, id)

	print('edit' in str(data))
	postfix = ''
	if('edit' in str(data)):
		postfix = 'edit_{}'.format(query.data.split('edit_')[1])
		datesh = DateTimeScheduler.get(DateTimeScheduler.id == query.data.split('edit_')[1])
		datesh.hour = int(hour)
		datesh.save()
	else:
		datesh = DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id, DateTimeScheduler.num_day == int(day), DateTimeScheduler.hour == int(hour), DateTimeScheduler.state == False)
		if(not datesh):
			print(294)
			scheduler = Scheduler.get(Scheduler.id == id)
			len_sh = DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id).count()
			if(len_sh < 7):
				DateTimeScheduler.create(scheduler=scheduler, num_day=int(day), hour=int(hour))
			else:
				print(340)
				# update.callback_query.answer('Ограничение: 7 напоминаний на заметку', show_alert=True)
				context.bot.send_message(chat_id=query.message.chat_id, text='Ограничение: 7 напоминаний на заметку')
				return 'TIMING'

	buttons = []
	datesh = DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id)
	for x in range(0, 60, 5):
		prefix = ''
		for y in datesh:
			if(y.hour == int(hour) and day == y.num_day and y.minute == x):
				prefix = '✅'
		buttons.append(InlineKeyboardButton('{}{}'.format(prefix, x), callback_data='112_{}_{}_{}_{}_{}'.format(id, day, hour, x, postfix)))
	keyboard = settings.constructor(buttons, 6)
	# keyboard = settings.constructor(buttons, settings.COUNT_ROW)
	reply_markup = InlineKeyboardMarkup(keyboard)

	buttons = []
	if(DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id, DateTimeScheduler.num_day != None, DateTimeScheduler.hour != None, DateTimeScheduler.minute != None, DateTimeScheduler.state == False)):
		reply_markup.inline_keyboard.append([InlineKeyboardButton("↩️ Часы", callback_data='110_{}_{}_out_{}'.format(id, day, postfix))])
		reply_markup.inline_keyboard.append([InlineKeyboardButton("Готово", callback_data='114_{}'.format(id))])
	else:
		reply_markup.inline_keyboard.append([InlineKeyboardButton("↩️ Часы", callback_data='110_{}_{}_out_{}'.format(id, day, postfix))])

	reply_markup.inline_keyboard.append([InlineKeyboardButton("↩️ Назад", callback_data='103_{}'.format(id))])

	context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup, media=InputMediaPhoto(media=notes.scheduler.file_patch, caption='День недели: *{}*\n*{}* {}\nВыберите минуту'.format(DAYS[int(day)], hour, HOUR[int(hour)]), parse_mode='Markdown'))

	return 'TIMING'

def minute_add(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	day = data[2]
	hour = data[3]
	minute = data[4]
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client, id)

	print(381, 'edit' in str(data))
	postfix = ''
	if('edit' in str(data)):
		postfix = 'edit_{}'.format(query.data.split('edit_')[1])
		datesh = DateTimeScheduler.get(DateTimeScheduler.id == query.data.split('edit_')[1])
		datesh.minute = minute
		datesh.save()
	else:
		datesh = DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id, DateTimeScheduler.minute == int(minute), DateTimeScheduler.num_day == int(day), DateTimeScheduler.hour == int(hour), DateTimeScheduler.state == False)
		if(datesh):
			datesh[0].minute = None
			datesh[0].save()
		else:
			datesh = DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id, DateTimeScheduler.minute == None, DateTimeScheduler.num_day == int(day), DateTimeScheduler.hour == int(hour), DateTimeScheduler.state == False)
			print(datesh)
			if(datesh):
				datesh[0].minute = int(minute)
				datesh[0].save()
			else:
				scheduler = Scheduler.get(Scheduler.id == id)
				len_sh = DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id).count()
				print(402, len_sh)
				if(len_sh < 7):
					DateTimeScheduler.create(scheduler=scheduler, minute=int(minute), num_day=int(day), hour=int(hour))
				else:
					# context.bot.answer_callback_query(callback_query_id=update.callback_query.id, text='Ограничение: 7 напоминаний на заметку')
					context.bot.send_message(chat_id=query.message.chat_id, text='Ограничение: 7 напоминаний на заметку')
					return 'TIMING'
	buttons = []
	datesh = DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id)
	for x in range(0, 60, 5):
		prefix = ''
		for y in datesh:
			if(y.hour == int(hour) and day == y.num_day and y.minute == x):
				prefix = '✅'
		buttons.append(InlineKeyboardButton('{}{}'.format(prefix, x), callback_data='112_{}_{}_{}_{}'.format(id, day, hour, x)))
	keyboard = settings.constructor(buttons, 6)
	# keyboard = settings.constructor(buttons, settings.COUNT_ROW)
	reply_markup = InlineKeyboardMarkup(keyboard)

	buttons = []
	if('edit' not in str(data) and DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id, DateTimeScheduler.num_day != None, DateTimeScheduler.hour != None, DateTimeScheduler.minute != None, DateTimeScheduler.state == False)):
		reply_markup.inline_keyboard.append([InlineKeyboardButton("↩️ Часы", callback_data='110_{}_{}_out_{}'.format(id, day, postfix))])
		reply_markup.inline_keyboard.append([InlineKeyboardButton("Готово", callback_data='114_{}'.format(id))])
	else:
		reply_markup.inline_keyboard.append([InlineKeyboardButton("↩️ Часы", callback_data='110_{}_{}_out_{}'.format(id, day, postfix))])

	reply_markup.inline_keyboard.append([InlineKeyboardButton("↩️ Назад", callback_data='103_{}'.format(id))])
	context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup, media=InputMediaPhoto(media=notes.scheduler.file_patch, caption='День недели: *{}*\n*{}* {}\nВыберите минуту'.format(DAYS[int(day)], hour, HOUR[int(hour)]), parse_mode='Markdown'))
	return 'TIMING'

def date_add(update, context):
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client, id)
	req = DateTimeScheduler.update(state=True).where(DateTimeScheduler.scheduler_id == id, DateTimeScheduler.minute != None)
	req.execute()
	notes.detail(id)

	context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=notes.reply_markup, media=InputMediaPhoto(media=notes.scheduler.file_patch, caption=notes.scheduler.body), parse_mode='Markdown')
	return 'TIMING'

def date_delete(update, context):
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	sh_id = int(data[2])
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client, id)
	req = DateTimeScheduler.delete().where(DateTimeScheduler.id == id)
	req.execute()
	notes.detail(sh_id)

	context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=notes.reply_markup, media=InputMediaPhoto(media=notes.scheduler.file_patch, caption=notes.scheduler.body), parse_mode='Markdown')
	return 'TIMING'

def settings_mode(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	mode = data[2]
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client, id)
	notes.update('mode', id, mode)
	notes.detail(id)

	context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=notes.reply_markup, media=InputMediaPhoto(media=notes.scheduler.file_patch, caption=notes.scheduler.body), parse_mode='Markdown')
	return 'TIMING'

def settings_name(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client, id)
	user.create_dialog('TIMING|108|{}'.format(id))

	context.bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)
	context.bot.send_message(chat_id=query.message.chat.id, text='Введите текст напоминания', parse_mode='Markdown')
	return 'TIMING'

def stopnoti(update, context):
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	DateTimeScheduler.delete().join(Scheduler).where(DateTimeScheduler.scheduler_id == id)
	query.edit_message_text(
		"Оповещение отключено",
	)
	return 'TIMING'

def stopimpo(update, context):
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	imp = Important.get(Important.id == id)
	imp.day = None
	imp.month = None
	imp.hour = None
	imp.minute = None
	imp.save()

	query.edit_message_text(
		"Оповещение отключено",
	)
	return 'TIMING'

def important(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	user = UsersClass(query.from_user.id)
	notes = ImportantClass(user.client, None)
	if('_' in query.data):
		notes.get({'page': 1, 'count': settings.COUNT_PAGE, 'note_id': query.data.split('_')[1]})
	else:
		notes.get({'page': 1, 'count': settings.COUNT_PAGE})

	if(notes.state):
		if(notes.important.file_patch):
			# context.bot.deleteMessage(chat_id=query.message.chat.id, message_id=update.message.message_id)
			context.bot.sendPhoto(chat_id=query.message.chat.id, photo=notes.important.file_patch, caption=notes.important.body, reply_markup=notes.reply_markup, parse_mode='Markdown')
		else:
			query.edit_message_text(
				text=notes.important.body,
				reply_markup=notes.reply_markup,
				parse_mode='Markdown'
			)
		return 'TIMING'
	else:
		user.create_dialog('TIMING|200')

		buttons = [
				InlineKeyboardButton("Отменить ❌", callback_data='777'),
		]
		keyboard = settings.constructor(buttons, settings.COUNT_ROW)
		reply_markup = InlineKeyboardMarkup(keyboard)
		query.edit_message_text(
			'Введите текст напоминания или отправьте картинку',
			reply_markup=reply_markup,
			parse_mode='Markdown'
		)
		return 'DIALOG'

def importantpagin(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	print(data)
	page = int(data[1])

	user = UsersClass(query.from_user.id)
	notes = ImportantClass(user.client, None)
	notes.get({'page': page, 'count': settings.COUNT_PAGE})
	if(notes.state):
		context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=notes.reply_markup, media=InputMediaPhoto(media=notes.important.file_patch, caption=notes.important.body, parse_mode='Markdown'))
		return 'TIMING'
	else:
		user.create_dialog('TIMING|200')
		context.bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)
		context.bot.send_message(chat_id=query.message.chat.id, text='Введите текст напоминания или отправьте картинку', parse_mode='Markdown')
		return 'DIALOG'

def importantcreate(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	user = UsersClass(query.from_user.id)
	user.create_dialog('TIMING|200')
	context.bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)
	context.bot.send_message(chat_id=query.message.chat.id, text='Введите текст напоминания или отправьте картинку', parse_mode='Markdown')
	return 'DIALOG'

def importantdelete(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = ImportantClass(user.client, None)
	notes.delete(id)
	notes.get({'page': 1, 'count': settings.COUNT_PAGE})

	if(notes.state):
		context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=notes.reply_markup, media=InputMediaPhoto(media=notes.important.file_patch, caption=notes.important.body, parse_mode='Markdown'))
		return 'TIMING'
	else:
		buttons = [
			InlineKeyboardButton("📝 Планировщик", callback_data='100'),
			InlineKeyboardButton("📝 Важные даты", callback_data='200'),
		]
		keyboard = settings.constructor(buttons, settings.COUNT_ROW)
		reply_markup = InlineKeyboardMarkup(keyboard)
		
		context.bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)
		context.bot.send_message(chat_id=query.message.chat.id, text="Это ваш персональный планировщик дел на день, неделю, месяц и квартал", reply_markup=reply_markup, parse_mode='Markdown')
	return 'TIMING'

def importantdetail(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = ImportantClass(user.client, id)
	notes.detail(id)

	context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=notes.reply_markup, media=InputMediaPhoto(media=notes.important.file_patch, caption=notes.important.body), parse_mode='Markdown')
	return 'TIMING'

def importantmode(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = ImportantClass(user.client, id)

	buttons = []
	for x in MODE_IMPORTANT:
		buttons.append(InlineKeyboardButton(MODE_IMPORTANT[x], callback_data='209_{}_{}'.format(id, x)))
	keyboard = settings.constructor(buttons, settings.COUNT_ROW)
	reply_markup = InlineKeyboardMarkup(keyboard)

	context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup, media=InputMediaPhoto(media=notes.important.file_patch, caption='Выберите режим работы'), parse_mode='Markdown')
	return 'TIMING'

def settings_mode_important(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	period = data[2]
	user = UsersClass(query.from_user.id)
	notes = ImportantClass(user.client, id)
	notes.update('mode', id, period)
	notes.detail(id)

	context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=notes.reply_markup, media=InputMediaPhoto(media=notes.important.file_patch, caption=notes.important.body), parse_mode='Markdown')
	return 'TIMING'

def settings_importantname(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = ImportantClass(user.client, id)
	user.create_dialog('TIMING|208|{}'.format(id))

	context.bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)
	context.bot.send_message(chat_id=query.message.chat.id, text='Введите текст напоминания', parse_mode='Markdown')
	return 'TIMING'

def settings_importantdate(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = ImportantClass(user.client, id)
	user.create_dialog('TIMING|209|{}'.format(id))

	context.bot.deleteMessage(chat_id=query.message.chat_id, message_id=query.message.message_id)
	context.bot.send_message(chat_id=query.message.chat.id, text='Введите дату в формате дд.мм', parse_mode='Markdown')
	return 'TIMING'

def hour_importantdetail(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = ImportantClass(user.client, id)
	
	buttons = []
	for x in range(1, 24):
		prefix = ''
		if(notes.important.hour == x):
			prefix = '✅'

		buttons.append(InlineKeyboardButton('{}{}'.format(prefix, x), callback_data='211_{}_{}'.format(id, x)))

	keyboard = settings.constructor(buttons, 4)
	reply_markup = InlineKeyboardMarkup(keyboard)

	reply_markup.inline_keyboard.append([InlineKeyboardButton("↩️ Назад", callback_data='203_{}'.format(id))])
	context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup, media=InputMediaPhoto(media=notes.important.file_patch, caption='Выберите час', parse_mode='Markdown'))

	return 'TIMING'

def minute_importantdetail(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	hour = data[2]
	user = UsersClass(query.from_user.id)
	notes = ImportantClass(user.client, id)

	buttons = []
	for x in range(0, 60, 5):
		prefix = ''
		if(notes.important.hour == x):
			prefix = '✅'

		buttons.append(InlineKeyboardButton('{}{}'.format(prefix, x), callback_data='212_{}_{}_{}'.format(id, hour, x)))

	keyboard = settings.constructor(buttons, 4)
	reply_markup = InlineKeyboardMarkup(keyboard)

	reply_markup.inline_keyboard.append([InlineKeyboardButton("↩️ Назад", callback_data='203_{}'.format(id))])
	context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=reply_markup, media=InputMediaPhoto(media=notes.important.file_patch, caption='*{} {}*\nВыберите минуту'.format(hour, HOUR[int(hour)]), parse_mode='Markdown'))

	return 'TIMING'

def minute_importantadd(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	hour = data[2]
	minute = data[3]
	user = UsersClass(query.from_user.id)
	notes = ImportantClass(user.client, id)

	notes.update(type_up='hour&minute', id=id, data=[hour, minute])
	notes.detail(id)
	context.bot.edit_message_media(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=notes.reply_markup, media=InputMediaPhoto(media=notes.important.file_patch, caption=notes.important.body, parse_mode='Markdown'))
	return 'TIMING'
