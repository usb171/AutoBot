from comtypes.client import CreateObject, ShowEvents, PumpEvents, GetEvents


class E3DataAccess(object):


    def __init__(self, host='localhost'):
        super(E3DataAccess, self).__init__()
        self._engine = CreateObject("{80327130-FFDB-4506-B160-B9F8DB32DFB2}")
        self._engine.Server = host


    def registerCallback(self, path):
        return self._engine.RegisterCallback(path)


    def unregisterCallback(self, path):
        return self._engine.UnregisterCallback(path)
        

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


    def executeQuery(self, pathname, Names=[''], Values=['']):
        return self._engine.ExecuteQuery(pathname, Names, Values)


    def writevalue(self, pathname, date, quality, value):
        try:
            self._engine.WriteValue(pathname, date, quality, value)
        except Exception as e:
            print(e)


    def closeConnect(self):
        del self._engine


    def onValueChanged(self, object):
        return GetEvents(self._engine, object)


    def pumpEventsChanged(self, time):
        return PumpEvents(time)
