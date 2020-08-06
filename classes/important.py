# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from models import *
import settings
import pytz

class ImportantClass:

	def __init__(self, client, id):
		self.client = client
		if(id):
			self.important = Important.get(Important.id == id)

	def get(self, paginate):
		self.state = False
		self.important_count = Important.select().join(Clients).where(Clients.id == self.client.id).count()
		print(paginate)
		if(self.important_count != 0):
			self.state = True
			if('note_id' in paginate):
				for x in range(1, self.important_count+1):
					for y in Important.select().join(Clients).where(Clients.id == self.client.id).order_by(Important.id.desc()).paginate(x, paginate['count']):
						if(int(paginate['note_id']) == y.id):
							self.important = Important.select().join(Clients).where(Clients.id == self.client.id).order_by(Important.id.desc()).paginate(x, paginate['count'])
							page = x
							break
			else:
				page = paginate['page']
				self.important = Important.select().join(Clients).where(Clients.id == self.client.id).order_by(Important.id.desc()).paginate(page, paginate['count'])

			buttons = []
			print(self.important)
			self.important = self.important[0]
			print(self.important)
			
			if page > 1:
				buttons.append(InlineKeyboardButton("<<", callback_data='201_{}'.format(page - 1)))
			else:
				buttons.append(InlineKeyboardButton("<<", callback_data='201_{}'.format(self.important_count)))

			buttons.append(InlineKeyboardButton("{}/{}".format(page, self.important_count), callback_data='-'))

			if page < self.important_count:
				buttons.append(InlineKeyboardButton(">>", callback_data='201_{}'.format(page + 1)))
			else:
				buttons.append(InlineKeyboardButton(">>", callback_data='201_{}'.format(1)))

			buttons.append(InlineKeyboardButton("🔧 Настройки", callback_data='203_{}'.format(self.important.id)))
			buttons.append(InlineKeyboardButton("✅ Добавить", callback_data='204'))
			keyboard = settings.constructor(buttons, 3)
			self.reply_markup = InlineKeyboardMarkup(keyboard)
			self.reply_markup.inline_keyboard.append([InlineKeyboardButton("❌ Удалить", callback_data='205_{}'.format(self.important.id))])
			# self.reply_markup.inline_keyboard.append([InlineKeyboardButton("↩️ Назад", callback_data='888')])

	def detail(self, id):
		print(54, self.important.file_patch)
		buttons = []
		buttons.append(InlineKeyboardButton("Переименовать", callback_data='208_{}'.format(self.important.id)))
		keyboard = settings.constructor(buttons, settings.COUNT_ROW)
		self.reply_markup = InlineKeyboardMarkup(keyboard)
		buttons = []
		self.reply_markup.inline_keyboard.append([InlineKeyboardButton('Режим: ' + MODE_IMPORTANT[self.important.mode] if self.important.mode else "Режим", callback_data='206_{}'.format(self.important.id))])
		if(self.important.day and self.important.month):
			now = datetime.datetime.now(pytz.timezone('Europe/Kiev'))
			str_day = '0' + str(self.important.day) if int(self.important.day) < 10 else str(self.important.day)
			str_month = '0' + str(self.important.month) if int(self.important.month) < 10 else str(self.important.month)
			buttons.append(InlineKeyboardButton(str_day + '.' + str_month, callback_data='207_{}'.format(self.important.id)))
		else:
			buttons.append(InlineKeyboardButton('Указать дату', callback_data='207_{}'.format(self.important.id)))
		
		if(self.important.hour and self.important.minute):
			str_time = str(datetime.time(int(self.important.hour), int(self.important.minute)))
			if(len(str_time.split(':')) == 3): 
				str_time = str_time.replace(':00', '')
			buttons.append(InlineKeyboardButton(str_time, callback_data='210_{}'.format(self.important.id)))
		else:
			buttons.append(InlineKeyboardButton('Указать время', callback_data='210_{}'.format(self.important.id)))

		self.reply_markup.inline_keyboard.append(buttons)
		self.reply_markup.inline_keyboard.append([InlineKeyboardButton("↩️ Назад", callback_data='200_{}'.format(self.important.id))])

	def create(self, message, file=None):
		if(file):
			self.important = Important.create(client=self.client, file_patch=file)
		else:
			self.important = Important.select().where(Important.body == None)
			if(self.important):
				self.important = self.important[0]
				self.important.body = message
				self.important.save()
			else:
				self.important = Important.create(body=message, client=self.client)

	def update(self, type_up, id, data):
		print(id)
		self.important = Important.get(Important.id == id)
		if(type_up == 'body'): self.important.body = data
		if(type_up == 'mode'): self.important.mode = data
		if(type_up == 'date'): 
			self.important.day = data[0]
			self.important.month = data[1]
		if(type_up == 'hour&minute'): 
			self.important.hour = data[0]
			self.important.minute = data[1]

		self.important.send = False
		self.important.end = False
		self.important.time_send = None
		self.important.save()

	def delete(self, id):
		print(id)
		Important.get(Important.id == id).delete_instance()
