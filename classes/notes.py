# -*- coding: utf-8 -*-
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from models import *
import settings

class NotesClass:

	def __init__(self, client):
		self.client = client

	def get(self, paginate):
		self.state = False
		self.scheduler = Scheduler.select().join(Clients).where(Clients.id == self.client.id).order_by(Scheduler.id.desc()).paginate(paginate['page'], paginate['count'])
		self.scheduler_count = Scheduler.select().join(Clients).where(Clients.id == self.client.id).count()
		if(self.scheduler):
			self.scheduler = self.scheduler[0]
			self.state = True
			buttons = []
			if paginate['page'] > 1:
				buttons.append(InlineKeyboardButton("<<", callback_data='101_{}'.format(paginate['page'] - 1)))

			buttons.append(InlineKeyboardButton("{}/{}".format(paginate['page'], self.scheduler_count), callback_data='-'))

			if paginate['page'] < self.scheduler_count:
				buttons.append(InlineKeyboardButton(">>", callback_data='101_{}'.format(paginate['page'] + 1)))

			keyboard = settings.constructor(buttons, 3)
			self.reply_markup = InlineKeyboardMarkup(keyboard)
			self.reply_markup.inline_keyboard.append([InlineKeyboardButton("Настройки", callback_data='103_{}'.format(self.scheduler.id))])
			self.reply_markup.inline_keyboard.append([InlineKeyboardButton("Удалить", callback_data='105_{}'.format(self.scheduler.id))])
			self.reply_markup.inline_keyboard.append([InlineKeyboardButton("Добавить", callback_data='104')])

	def detail(self, id):
		self.scheduler = Scheduler.get(Scheduler.id == id)

		buttons = []
		buttons.append(InlineKeyboardButton("Название", callback_data='108_{}'.format(self.scheduler.id)))
		keyboard = settings.constructor(buttons, settings.COUNT_ROW)
		self.reply_markup = InlineKeyboardMarkup(keyboard)
		self.reply_markup.inline_keyboard.append([InlineKeyboardButton(MODE[self.scheduler.mode] if self.scheduler.mode else "Как часто", callback_data='106_{}'.format(self.scheduler.id))])
		self.dash = DateTimeScheduler.select().join(Scheduler).where(Scheduler.id == id, DateTimeScheduler.state == True)
		if(self.dash):
			for x in self.dash:
				buttons = [
					InlineKeyboardButton(DAYS[int(x.num_day)], callback_data='-'),
					InlineKeyboardButton('{}:{}'.format(x.hour, x.minute), callback_data='-'),
					InlineKeyboardButton('❌', callback_data='115_{}_{}'.format(x.id, self.scheduler.id))
				]

				self.reply_markup.inline_keyboard.append(buttons)

		if(len(self.dash) < 7):
			self.reply_markup.inline_keyboard.append([InlineKeyboardButton("Когда", callback_data='107_{}'.format(self.scheduler.id))])

	def create(self, message):
		self.scheduler = Scheduler.create(body=message, client=self.client)

	def update(self, type_up, id, data):
		print(id)
		self.scheduler = Scheduler.get(Scheduler.id == id)
		if(type_up == 'body'): self.scheduler.body = data
		if(type_up == 'mode'): self.scheduler.mode = data
		self.scheduler.save()

	def delete(self, id):
		print(id)
		Scheduler.get(Scheduler.id == id).delete_instance()
