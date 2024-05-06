class Journey:
    def __init__(self, start_alpha3, end_alpha3, departure, arrival):
        self._start_alpha3 = start_alpha3  ## string: 3 letter code for the start station
        self._end_alpha3 = end_alpha3  ## string: 3 letter code for the end station
        self._departure = departure  ## datetime: departure date and time
        self._arrival = arrival  ## datetime: arrival date and time

    def getStartAlpha3(self):   return self._start_alpha3

    def getEndAlpha3(self):     return self._end_alpha3

    def getDeparture(self):     return self._departure

    def getArrival(self):       return self._arrival

    def setStartAlpha3(self, start_alpha3): self._start_alpha3 = start_alpha3

    def setEndAlpha3(self, end_alpha3):     self._end_alpha3 = end_alpha3

    def setDeparture(self, departure):      self._departure = departure

    def setArrival(self, arrival):          self._arrival = arrival