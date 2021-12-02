import time
import json
import requests


class Telegram(object):


	def __init__(self, token, chatID, Elipse, timeout=100):
		super(Telegram, self).__init__()
		self._token = token
		self._chatID = chatID
		self._url = 'https://api.telegram.org/bot{}/'.format(token)
		self._timeout = timeout
		self._Elipse = Elipse


	def updateToken(self, token):
		self._token = token


	def updateChatID(self, chatID):
		self._chatID = chatID


	def runPooling(self):
		updateID = None
		while True:
			#print(time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime()), '-> Bot Online')
			try:
				messages = self.getMessages(updateID)
				if messages:
					for message in messages:
						updateID = self.getUpdateID(message)
						chatID = self.getChatIDMessages(message)
						text = self.getTextMessages(message)
						print(text)
						action = text[0]
					if action.lower() == '/ler':
						SE = text[1]
						BAY = text[2]
						EQ = text[3]
						print(action, SE, BAY, EQ)
						self.sendMessage(self._Elipse.getAll(SE=SE, BAY=BAY, EQ=EQ))
					elif action.lower() == '/com':
						self.sendMesse(self._Elipse.getCOM())
					elif action.lower() == '/mapa':
						self.sendImage()
					elif action.lower() == '/dom':
						self.sendMessage(self._Elipse.getDOM())
					elif action.lower() == '/rt':
						tag = text[1]
						print('Registrando a TAG: ', tag, self._Elipse.registerCallback(tag))
						self.sendMessage('Tag ' + tag + ' registrada com sucesso!')
					elif action.lower() == '/urt':
						tag = text[1]
						print('Cancelando o registro da TAG: ', tag, self._Elipse.unregisterCallback(tag))
						self.sendMessage('Tag ' + tag + ' cancelada o registro com sucesso!')



			except Exception as e:
				print(f'Erro: {e}')
				self.sendMessage(f'Comando inválido!!\n{e}', self._chatID)
			time.sleep(1)


	def getTextMessages(self, message):
		return message['message']['text'].split(' ')


	def getChatIDMessages(self, message):
		return message['message']['from']['id']


	def getUpdateID(self, message):
		return message['update_id']


	def sendMessage(self, text, chatID=None):
		url = self._url + 'sendMessage?chat_id={chatID}&text={text}'
		url = url.format(chatID=self._chatID if chatID is None else chatID, text=text)
		return requests.get(url).json()


	def sendMessageHTML(self, text, chatID=None):
		url = self._url + 'sendMessage?chat_id={chatID}&parse_mode=HTML&text={text}'
		url = url.format(chatID=self._chatID if chatID is None else chatID, text=text)
		print(url)
		return requests.get(url).json()


	def getMessages(self, updateID):
		url = self._url + 'getUpdates?timeout={}'.format(self._timeout)
		if updateID:
			url = url + '&offset={}'.format(updateID + 1)
		result = requests.get(url)
		return json.loads(result.content).get('result')
