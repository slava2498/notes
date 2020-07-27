# -*- coding: utf-8 -*-
from models import *

class UsersClass:

	def __init__(self, chat_id):
		self.client = Clients.select().where(Clients.chat_id == chat_id)
		if(self.client):
			self.client = self.client[0]
			dialog = DialogControll.select().join(Clients).where(Clients.id == self.client.id)
			if(dialog):
				self.dialog = dialog[0]
			else:
				self.dialog = None
		else:
			self.client = Clients.create(chat_id=chat_id)
			self.dialog = None

	def create_dialog(self, data):
		self.dialog = DialogControll.create(client=self.client, data=data)

	def delete_dialog(self):
		if(self.dialog):
			self.dialog.delete_instance()
			self.dialog = None