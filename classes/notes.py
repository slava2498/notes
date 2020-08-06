# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from models import *
import settings

class NotesClass:

	def __init__(self, client, id):
		self.client = client
		if(id):
			self.scheduler = Scheduler.get(Scheduler.id == id)

	def get(self, paginate):
		self.state = False
		self.scheduler_count = Scheduler.select().join(Clients).where(Clients.id == self.client.id).count()
		print(paginate)
		if(self.scheduler_count != 0):
			self.state = True
			if('note_id' in paginate):
				for x in range(1, self.scheduler_count+1):
					for y in Scheduler.select().join(Clients).where(Clients.id == self.client.id).order_by(Scheduler.id.desc()).paginate(x, paginate['count']):
						if(int(paginate['note_id']) == y.id):
							self.scheduler = Scheduler.select().join(Clients).where(Clients.id == self.client.id).order_by(Scheduler.id.desc()).paginate(x, paginate['count'])
							page = x
							break
			else:
				page = paginate['page']
				self.scheduler = Scheduler.select().join(Clients).where(Clients.id == self.client.id).order_by(Scheduler.id.desc()).paginate(page, paginate['count'])

			buttons = []
			print(self.scheduler)
			self.scheduler = self.scheduler[0]
			print(self.scheduler)
			
			if page > 1:
				buttons.append(InlineKeyboardButton("<<", callback_data='101_{}'.format(page - 1)))
			else:
				buttons.append(InlineKeyboardButton("<<", callback_data='101_{}'.format(self.scheduler_count)))

			buttons.append(InlineKeyboardButton("{}/{}".format(page, self.scheduler_count), callback_data='-'))

			if page < self.scheduler_count:
				buttons.append(InlineKeyboardButton(">>", callback_data='101_{}'.format(page + 1)))
			else:
				buttons.append(InlineKeyboardButton(">>", callback_data='101_{}'.format(1)))

			buttons.append(InlineKeyboardButton("🔧 Настройки", callback_data='103_{}'.format(self.scheduler.id)))
			buttons.append(InlineKeyboardButton("✅ Добавить", callback_data='104'))
			keyboard = settings.constructor(buttons, 3)
			self.reply_markup = InlineKeyboardMarkup(keyboard)
			self.reply_markup.inline_keyboard.append([InlineKeyboardButton("❌ Удалить", callback_data='105_{}'.format(self.scheduler.id))])
			# self.reply_markup.inline_keyboard.append([InlineKeyboardButton("↩️ Назад", callback_data='888')])

	def detail(self, id):
		print(54, self.scheduler.file_patch)
		buttons = []
		buttons.append(InlineKeyboardButton("Переименовать", callback_data='108_{}'.format(self.scheduler.id)))
		keyboard = settings.constructor(buttons, settings.COUNT_ROW)
		self.reply_markup = InlineKeyboardMarkup(keyboard)
		self.reply_markup.inline_keyboard.append([InlineKeyboardButton('Режим: ' + MODE[self.scheduler.mode] if self.scheduler.mode else "Режим", callback_data='106_{}'.format(self.scheduler.id))])
		self.reply_markup.inline_keyboard.append([InlineKeyboardButton('Период: ' + PERIOD[self.scheduler.period] if self.scheduler.period else "Период", callback_data='199_{}'.format(self.scheduler.id))])
		self.dash = DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id, DateTimeScheduler.state == True)
		if(self.dash):
			for x in self.dash:
				str_time = str(datetime.time(x.hour, x.minute))
				if(len(str_time.split(':')) == 3): 
					str_time = str_time.replace(':00', '')
				buttons = [
					InlineKeyboardButton(DAYS[int(x.num_day)], callback_data='107_{}_edit_{}'.format(self.scheduler.id, x.id)),
					InlineKeyboardButton(str_time, callback_data='110_{}_{}_edittime_{}'.format(self.scheduler.id, x.num_day, x.id)),
					InlineKeyboardButton('❌', callback_data='115_{}_{}'.format(x.id, self.scheduler.id))
				]

				self.reply_markup.inline_keyboard.append(buttons)

		if(len(self.dash) < 7):
			self.reply_markup.inline_keyboard.append([InlineKeyboardButton("День/Время", callback_data='107_{}'.format(self.scheduler.id))])

		self.reply_markup.inline_keyboard.append([InlineKeyboardButton("↩️ Назад", callback_data='100_{}'.format(self.scheduler.id))])

	def create(self, message, file=None):
		if(file):
			self.scheduler = Scheduler.create(client=self.client, file_patch=file)
		else:
			self.scheduler = Scheduler.select().where(Scheduler.body == None)
			if(self.scheduler):
				self.scheduler = self.scheduler[0]
				self.scheduler.body = message
				self.scheduler.save()
			else:
				self.scheduler = Scheduler.create(body=message, client=self.client)

	def update(self, type_up, id, data):
		print(id)
		self.scheduler = Scheduler.get(Scheduler.id == id)
		if(type_up == 'body'): self.scheduler.body = data
		if(type_up == 'mode'): self.scheduler.mode = data
		if(type_up == 'period'): self.scheduler.period = data
		self.scheduler.save()

	def delete(self, id):
		print(id)
		Scheduler.get(Scheduler.id == id).delete_instance()
