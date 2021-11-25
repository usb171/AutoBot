from comtypes.client import CreateObject, GetModule


class E3DataAccess(object):

	def __init__(self, UUID, host='localhost'):
		super(E3DataAccess, self).__init__()
		self._engine = CreateObject(UUID)
		self._engine.Server = host
    

	def registerCallback(self, path):
		return self._engine.RegisterCallback(path)


	def updateHost(self, host):
		self._engine.Server = host
		return self._engine.Server


	def disconnect(self):
		return self._engine.Disconnect()


	def connect(self):
		return self._engine.Connect()


	def getDomainState(self):
		return self._engine.DomainState


	def readvalue(self, pathname):
		try:
			return self._engine.ReadValue(pathname)
		except Exception as e:
			print(e)


	def executeQuery(self, query):
		return self._engine.ExecuteQuery(query)


	def writevalue(self, pathname, date, quality, value):
		try:
			self._engine.WriteValue(pathname, date, quality, value)
		except Exception as e:
			print(e)

	def closeConnect(self):
		del self._engine


class Elipse(object):
	
	
	def __init__(self, UUID, host, template):
		super(Elipse, self).__init__()
		self._E3DataAccess = E3DataAccess(UUID=UUID, host=host)
		self._template = template


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