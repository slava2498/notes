from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
import settings
import logging
from models import *
from classes.user import UsersClass
from classes.notes import NotesClass

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)

def start_over(update, context):
	query = update.callback_query
	query.answer()
	buttons = [
		InlineKeyboardButton("Планировщик", callback_data='100'),
	]

	keyboard = settings.constructor(buttons, settings.COUNT_ROW)
	reply_markup = InlineKeyboardMarkup(keyboard)
	query.edit_message_text(
		text="Это ваш персональный планировщик дел на день, неделю, месяц и квартал",
		reply_markup=reply_markup
	)
	return 'TIMING'


def one(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client)
	notes.get({'page': 1, 'count': settings.COUNT_PAGE})
	if(notes.state):
		query.edit_message_text(
			text=notes.scheduler.body,
			reply_markup=notes.reply_markup
		)
		return 'TIMING'
	else:
		user.create_dialog('TIMING|104')

		buttons = [
				InlineKeyboardButton("Отменить", callback_data='777'),
		]
		keyboard = settings.constructor(buttons, settings.COUNT_ROW)
		reply_markup = InlineKeyboardMarkup(keyboard)
		query.edit_message_text(
			'Введите текст напоминания',
			reply_markup=reply_markup
		)
		return 'DIALOG'

def pagin(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	page = int(data[1])

	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client)
	notes.get({'page': page, 'count': settings.COUNT_PAGE})
	if(notes.state):
		query.edit_message_text(
			text=notes.scheduler.body,
			reply_markup=notes.reply_markup
		)
		return 'TIMING'
	else:
		user.create_dialog('TIMING|104')
		query.edit_message_text('Введите текст напоминания')
		return 'DIALOG'

def create(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	user = UsersClass(query.from_user.id)
	user.create_dialog('TIMING|104')
	query.edit_message_text('Введите текст напоминания')
	return 'DIALOG'

def delete(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client)
	notes.delete(id)
	notes.get({'page': 1, 'count': settings.COUNT_PAGE})
	if(notes.state):
		query.edit_message_text(
			text=notes.scheduler.body,
			reply_markup=notes.reply_markup
		)
		return 'TIMING'
	else:
		buttons = [
			InlineKeyboardButton("Планировщик", callback_data='100'),
		]

		keyboard = settings.constructor(buttons, settings.COUNT_ROW)
		reply_markup = InlineKeyboardMarkup(keyboard)
		query.edit_message_text(
			text="Это ваш персональный планировщик дел на день, неделю, месяц и квартал",
			reply_markup=reply_markup
		)
		return 'TIMING'

def stop(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	user = UsersClass(query.from_user.id)
	user.delete_dialog()
	query.edit_message_text(
		text="Действие отменено",
	)
	return 'TIMING'

def settings_detail(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client)
	notes.detail(id)

	query.edit_message_text(
		text=notes.scheduler.body,
		reply_markup=notes.reply_markup
	)
	return 'TIMING'

def mode_detail(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client)

	buttons = []
	for x in MODE:
		buttons.append(InlineKeyboardButton(MODE[x], callback_data='109_{}_{}'.format(id, x)))
	keyboard = settings.constructor(buttons, settings.COUNT_ROW)
	reply_markup = InlineKeyboardMarkup(keyboard)

	query.edit_message_text(
		text='Выберите режим работы',
		reply_markup=reply_markup
	)
	return 'TIMING'

def date_detail(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client)

	req = DateTimeScheduler.delete().where(DateTimeScheduler.state == False)
	req.execute()

	scheduler = Scheduler.get(Scheduler.id == id)
	DateTimeScheduler.create(scheduler=scheduler)
	buttons = []
	for x in DAYS:
		buttons.append(InlineKeyboardButton(DAYS[x], callback_data='110_{}_{}_in'.format(id, x)))
	keyboard = settings.constructor(buttons, settings.COUNT_ROW)
	reply_markup = InlineKeyboardMarkup(keyboard)

	query.edit_message_text(
		text='Выберите день недели',
		reply_markup=reply_markup
	)
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
	notes = NotesClass(user.client)

	if(call == 'in'):
		datesh = DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id, DateTimeScheduler.state == False)
		if(datesh):
			datesh = datesh[0]
			datesh.num_day = int(day)
			datesh.save()

	buttons = []
	datesh = DateTimeScheduler.select().where(DateTimeScheduler.scheduler_id == id)
	for x in range(1, 25):
		prefix = ''
		for y in datesh:
			if(y.hour == x and day == y.num_day):
				prefix = '✅'
		buttons.append(InlineKeyboardButton('{}{}'.format(prefix, x), callback_data='111_{}_{}_{}'.format(id, day, x)))

	keyboard = settings.constructor(buttons, 4)
	reply_markup = InlineKeyboardMarkup(keyboard)

	if(DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id, DateTimeScheduler.num_day != None, DateTimeScheduler.hour != None, DateTimeScheduler.minute != None, DateTimeScheduler.state == False)):
		reply_markup.inline_keyboard.append([InlineKeyboardButton("Добавить", callback_data='114_{}'.format(id))])
	query.edit_message_text(
		text='День недели: *{}*\nВыберите час'.format(DAYS[int(day)]),
		reply_markup=reply_markup,
		parse_mode='Markdown',
	)
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
	notes = NotesClass(user.client)

	datesh = DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id, DateTimeScheduler.num_day == int(day), DateTimeScheduler.hour == int(hour), DateTimeScheduler.state == False)
	if(not datesh):
		scheduler = Scheduler.get(Scheduler.id == id)
		DateTimeScheduler.create(scheduler=scheduler, num_day=int(day), hour=int(hour))

	buttons = []
	datesh = DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id)
	for x in range(60):
		prefix = ''
		for y in datesh:
			if(y.hour == int(hour) and day == y.num_day and y.minute == x):
				prefix = '✅'
		buttons.append(InlineKeyboardButton('{}{}'.format(prefix, x), callback_data='112_{}_{}_{}_{}'.format(id, day, hour, x)))
	keyboard = settings.constructor(buttons, 6)
	# keyboard = settings.constructor(buttons, settings.COUNT_ROW)
	reply_markup = InlineKeyboardMarkup(keyboard)

	buttons = []
	if(DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id, DateTimeScheduler.num_day != None, DateTimeScheduler.hour != None, DateTimeScheduler.minute != None, DateTimeScheduler.state == False)):
		reply_markup.inline_keyboard.append([InlineKeyboardButton("↩️Часы", callback_data='110_{}_{}_out'.format(id, day))])
		reply_markup.inline_keyboard.append([InlineKeyboardButton("Добавить", callback_data='114_{}'.format(id))])
	else:
		reply_markup.inline_keyboard.append([InlineKeyboardButton("↩️Часы", callback_data='110_{}_{}_out'.format(id, day))])

	keyboard = settings.constructor(buttons, 2)
	query.edit_message_text(
		text='День недели: *{}*\n*{}* {}\nВыберите минуту'.format(DAYS[int(day)], hour, HOUR[int(hour)]),
		reply_markup=reply_markup,
		parse_mode='Markdown',
	)
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
	notes = NotesClass(user.client)

	datesh = DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id, DateTimeScheduler.minute == int(minute), DateTimeScheduler.num_day == int(day), DateTimeScheduler.hour == int(hour), DateTimeScheduler.state == False)
	if(datesh):
		datesh[0].minute = None
		datesh[0].save()
	else:
		datesh = DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id, DateTimeScheduler.minute == None, DateTimeScheduler.num_day == int(day), DateTimeScheduler.hour == int(hour), DateTimeScheduler.state == False)
		if(datesh):
			datesh[0].minute = int(minute)
			datesh[0].save()
		else:
			scheduler = Scheduler.get(Scheduler.id == id)
			DateTimeScheduler.create(scheduler=scheduler, minute=int(minute), num_day=int(day), hour=int(hour))

	buttons = []
	datesh = DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id)
	for x in range(1, 61):
		prefix = ''
		for y in datesh:
			if(y.hour == int(hour) and day == y.num_day and y.minute == x):
				prefix = '✅'
		buttons.append(InlineKeyboardButton('{}{}'.format(prefix, x), callback_data='112_{}_{}_{}_{}'.format(id, day, hour, x)))
	keyboard = settings.constructor(buttons, 6)
	# keyboard = settings.constructor(buttons, settings.COUNT_ROW)
	reply_markup = InlineKeyboardMarkup(keyboard)

	buttons = []
	if(DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id, DateTimeScheduler.num_day != None, DateTimeScheduler.hour != None, DateTimeScheduler.minute != None, DateTimeScheduler.state == False)):
		reply_markup.inline_keyboard.append([InlineKeyboardButton("↩️Часы", callback_data='110_{}_{}_out'.format(id, day))])
		reply_markup.inline_keyboard.append([InlineKeyboardButton("Добавить", callback_data='114_{}'.format(id))])
	else:
		reply_markup.inline_keyboard.append([InlineKeyboardButton("↩️Часы", callback_data='110_{}_{}_out'.format(id, day))])

	keyboard = settings.constructor(buttons, 2)
	query.edit_message_text(
		text='День недели: *{}*\n*{}* {}\nВыберите минуту'.format(DAYS[int(day)], hour, HOUR[int(hour)]),
		reply_markup=reply_markup,
		parse_mode='Markdown',
	)
	return 'TIMING'

def date_add(update, context):
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client)
	req = DateTimeScheduler.update(state=True).where(DateTimeScheduler.scheduler_id == id, DateTimeScheduler.minute != None)
	req.execute()
	notes.detail(id)

	query.edit_message_text(
		text=notes.scheduler.body,
		reply_markup=notes.reply_markup
	)
	return 'TIMING'

def date_delete(update, context):
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	sh_id = int(data[2])
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client)
	req = DateTimeScheduler.delete().where(DateTimeScheduler.id == id)
	req.execute()
	notes.detail(sh_id)

	query.edit_message_text(
		text=notes.scheduler.body,
		reply_markup=notes.reply_markup
	)
	return 'TIMING'

def settings_mode(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	mode = data[2]
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client)
	notes.update('mode', id, mode)
	notes.detail(id)
	query.edit_message_text(
		text=notes.scheduler.body,
		reply_markup=notes.reply_markup
	)
	return 'TIMING'

def settings_datetime(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client)
	notes.delete(id)
	notes.get({'page': 1, 'count': settings.COUNT_PAGE})
	return 'TIMING'

def settings_name(update, context):
	"""Show new choice of buttons"""
	query = update.callback_query
	query.answer()

	data = query.data.split('_')
	id = int(data[1])
	user = UsersClass(query.from_user.id)
	notes = NotesClass(user.client)
	user.create_dialog('TIMING|108|{}'.format(id))
	query.edit_message_text('Введите текст напоминания')
	return 'TIMING'