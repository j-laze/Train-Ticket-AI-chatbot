class Journey:
    def __init__(self, start_alpha3, end_alpha3, departure, arrival):
        self._start_alpha3 = start_alpha3  ## string: 3 letter code for the start station
        self._end_alpha3 = end_alpha3  ## string: 3 letter code for the end station
        self._departure = departure  ## datetime: departure date and time
        self._arrival = arrival  ## datetime: arrival date and time
