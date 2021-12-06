import time
from E3DataAccess import E3DataAccess
from comtypes.client import CreateObject, ShowEvents, PumpEvents, GetEvents


class Elipse(object):


	def __init__(self, host='localhost', template=None):
		super(Elipse, self).__init__()
		self._E3DataAccess = None
		self.error = False
		self._template = template
		############# Atributos de manipulação dos eventos Elipse ##############
		self._sinkEvents = EventSink()
		self._connectionEvents = None
		########################################################################
		try:
			self._E3DataAccess = E3DataAccess(host=host)
			self._connectionEvents = self._E3DataAccess.onValueChanged(self._sinkEvents)
		except Exception as e:
			print(e)
			self.error = True


	def updateHost(self, host):
		host = self._E3DataAccess.updateHost(host)
		print("Elipse -> Reconectado Host: ", host)
		return host


	def writeValue(self):
		self._E3DataAccess.writevalue(pathname="IEC61850.[IO.WorkOnline]", date="23/10/2021 00:29:56", quality=192, value="1")
		self._E3DataAccess.writevalue(pathname="IEC61850.[IO.Ethernet.MainIP]", date="23/10/2021 00:29:56", quality=192, value="127.0.0.2")
		self._E3DataAccess.writevalue(pathname="IEC61850.[IO.Log.Enable]", date="23/10/2021 00:29:56", quality=192, value="1")
		self._E3DataAccess.writevalue(pathname="IEC61850.[IO.WorkOnline]", date="23/10/2021 00:29:56", quality=192, value="0")
		self._E3DataAccess.writevalue(pathname="IEC61850.[IO.SetConfigurationParameters]", date="23/10/2021 00:29:56", quality=192, value="1")


	def registerCallback(self, path):
		print("Registrando: ", path)
		return self._E3DataAccess.registerCallback(path)

	def unregisterCallback(self, path):
		return self._E3DataAccess.unregisterCallback(path)


	def executeQuery(self, query):
		return self._E3DataAccess.executeQuery(query)


	def getDomainState(self):
		return self._E3DataAccess.getDomainState()


	def disconnect(self):
		return self._E3DataAccess.disconnect()


	def connect(self):
		return self._E3DataAccess.connect()


	def get_iA_disjuntor(self, SE, BAY, EQ):
		pathname = self._template.get('IA').format(SE=SE, BAY=BAY, EQ=EQ)
		return f'Corrente A: {self._E3DataAccess.readvalue(pathname)[2]} A'


	def get_iB_disjuntor(self, SE, BAY, EQ):
		pathname = self._template.get('IB').format(SE=SE, BAY=BAY, EQ=EQ)
		return f'Corrente B: {self._E3DataAccess.readvalue(pathname)[2]} A'


	def get_iC_disjuntor(self, SE, BAY, EQ):
		pathname = self._template.get('IC').format(SE=SE, BAY=BAY, EQ=EQ)
		return f'Corrente C: {self._E3DataAccess.readvalue(pathname)[2]} A'


	def get_currents(self, SE, BAY, EQ):
		IA = self._E3DataAccess.readvalue(self._template.get('IA').format(SE=SE, BAY=BAY, EQ=EQ))[2]
		IB = self._E3DataAccess.readvalue(self._template.get('IB').format(SE=SE, BAY=BAY, EQ=EQ))[2]
		IC = self._E3DataAccess.readvalue(self._template.get('IC').format(SE=SE, BAY=BAY, EQ=EQ))[2]
		return f'Equipamento: {EQ}\nIA: {IA}\nIB: {IB}\nIC: {IC}'


	def getCOM(self):
		LinkStatus = self._E3DataAccess.readvalue(self._template.get('LinkStatus'))[2]
		ComStatus = self._E3DataAccess.readvalue(self._template.get('ComStatus'))[2]
		ElipseStatus = self._E3DataAccess.readvalue(self._template.get('ElipseStatus'))[2]
		EqpsStatus = self._E3DataAccess.readvalue(self._template.get('EqpsStatus'))[2]
		return f'LinkStatus: {LinkStatus}\nComStatus: {ComStatus}\nElipseStatus: {ElipseStatus}\nEqpsStatus: {EqpsStatus}'


	def getDOM(self):
		statusDOM = "Em execução!" if self._E3DataAccess.getDomainState() == 3 else "Parado!"
		return f'Domínio: {statusDOM}\n'


	def getAll(self, SE, BAY, EQ):
		status = self._E3DataAccess.readvalue(self._template.get('status').format(SE=SE, BAY=BAY, EQ=EQ))[2]
		if status == 1:
			status = "Fechado"
		elif status == 0:
			status = "Aberto"
		else:
			status = "Nulo"
		IA = self._E3DataAccess.readvalue(self._template.get('IA').format(SE=SE, BAY=BAY, EQ=EQ))[2]
		IB = self._E3DataAccess.readvalue(self._template.get('IB').format(SE=SE, BAY=BAY, EQ=EQ))[2]
		IC = self._E3DataAccess.readvalue(self._template.get('IC').format(SE=SE, BAY=BAY, EQ=EQ))[2]
		VAB = self._E3DataAccess.readvalue(self._template.get('VAB').format(SE=SE, BAY=BAY, EQ=EQ))[2]
		VBC = self._E3DataAccess.readvalue(self._template.get('VBC').format(SE=SE, BAY=BAY, EQ=EQ))[2]
		VCA = self._E3DataAccess.readvalue(self._template.get('VCA').format(SE=SE, BAY=BAY, EQ=EQ))[2]
		return f'Equipamento: {EQ}\nStatus: {status}\nIA: {IA}\nIB: {IB}\nIC: {IC}\nVAB: {VAB}\nVBC: {VBC}\nVCA: {VCA}'


	def printTableQuery(self, q):
		try:
			if q[1]:
				q = list(q[0])

				print('colunas:', len(q), 'linhas', len(q[0]))

				for linha in range(len(q[0])):
				    aux = ''
				    for coluna in range(len(q)):
				        aux = aux + "\t" + str(q[coluna][linha])
				    print(aux)
		except Exception as e:
			print(e)


	def pumpEventsChanged(self, time=-1):
		self._E3DataAccess.pumpEventsChanged(time)


	def setObjectEventListSink(self, object):
		self._sinkEvents.setObjectEventListSink(object)


	def getObjectEventListSink(self):
		return self._sinkEvents.getObjectEventListSink()


	def setObjectEventMutexSink(self, object):
		self._sinkEvents.setObjectEventMutexSink(object)


	def getObjectEventMutexSink(self):
		return self._sinkEvents.getObjectEventMutexSink()


	def registerDevice(self, SE, BAY, EQ):
		#return list(map(lambda key: self.registerCallback(self._template['measurements'][key].format(SE=SE, BAY=BAY, EQ=EQ)), self._template.get('measurements')))
		return list(map(lambda key: self.registerCallback(self._template['measurements'][key]), self._template.get('measurements')))



class EventSink(object):

	def __init__(self, arg=None):
		super(EventSink, self).__init__()
		self.arg = arg
		self.eventList = []
		self.mutex = None


	def setObjectEventListSink(self, object):
		self.eventList = object


	def setObjectEventMutexSink(self, object):
		self.mutex = object


	def getObjectEventListSink(self):
		return self.eventList


	def getObjectEventMutexSink(self):
		return self.mutex
		

	def _IE3DataAccessManagerEvents_OnValueChanged(self, this, pathname, timestamp, quality, value):
		self.mutex.acquire()
		text = "{};{};\t{}".format(time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime()), pathname, value)
		print("+ ", text, " Buffer: ", len(self.eventList))
		self.eventList.append(text)
		self.mutex.release()
