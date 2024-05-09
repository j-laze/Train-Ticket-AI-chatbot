## TODO: add single/return attributes
class Enquiry:
    def __init__(self, time="", depart_or_arrive="", start_alpha3="", end_alpha3="", adults=1, children=0):
        self.time = time  ## datetime: date and time of the enquirey
        self.depart_or_arrive = depart_or_arrive  ## boolean: depart=true or arrive=false
        self.start_alpha3 = start_alpha3  ## string: 3 letter code for the start station
        self.end_alpha3 = end_alpha3  ## string: 3 letter code for the end station
        self.adults = adults  ## int: number of adults
        self.children = children  ## int: number of children

    def getTime(self):              return self.time

    def getDepartOrArrive(self):    return self.depart_or_arrive

    def getStartAlpha3(self):       return self.start_alpha3

    def getEndAlpha3(self):         return self.end_alpha3

    def getAdults(self):            return self.adults

    def getChildren(self):          return self.children

    def setTime(self, time):                        self.time = time

    def setDepartOrArrive(self, depart_or_arrive):  self.depart_or_arrive = depart_or_arrive

    def setStartAlpha3(self, start_alpha3):         self.start_alpha3 = start_alpha3

    def setEndAlpha3(self, end_alpha3):             self.end_alpha3 = end_alpha3

    def setAdults(self, adults):                    self.adults = adults

    def setChildren(self, children):
        self.children = children

    def __str__(self):
        return f"Time: {self.time}, Depart or Arrive: {self.depart_or_arrive}, Start Station: {self.start_alpha3}, End Station: {self.end_alpha3}, Adults: {self.adults}, Children: {self.children}"
