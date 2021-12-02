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


	def setObjectEventSink(self, object):
		self._sinkEvents.setObjectEventSink(object)


class EventSink(object):

	def __init__(self, arg=None):
		super(EventSink, self).__init__()
		self.arg = arg
		self.object = None

	def setObjectEventSink(self, object):
		self.object = object

	def _IE3DataAccessManagerEvents_OnValueChanged(self, this, pathname, timestamp, quality, value):
		print(self.object, pathname, value)
