from datetime import *

#------------------------------------------------------------------------------
class Event:
    """
    Clase que engloba las caracteristicas y metodos generales de cada evento
    """
    def __init__(self, name: str, dat: date, tim: time, durat: timedelta, typeEv: str):
        self.name : str = name # Identificador del evento
        self.date : date = date # Fecha en que se realiza el evento
        self.time : tuple(time, time) = (tim, tim + durat) # Hora de inicio y duracion del evento
        self.typeEvent : str = typeEv # Tipo de evento
    
    def __str__(self):
        return f"{chr(16)} {self.time[0]}-{self.time[1]} | '{self.typeEvent}: {self.name}'"

#------------------------------------------------------------------------------
class Schedule:
    def __init__(self, dat: date, resources: dict):
        self.date = dat.strftime('%B, %d, %Y')
        self.listEvents: list[dict] = []
        '''
        self.places : dict = resources["Espacios Fisicos"]
        self.equipsSound : dict = resources["Equipos Tecnicos"]["Sonido"]
        self.equipsLight : dict = resources["Equipos Tecnicos"]["Iluminacion"]
        self.equipsVideo : dict = resources["Equipos Tecnicos"]["Proyeccion de video"]
        self.equipsMusic : dict = resources["Equipos Tecnicos"]["Musica"]
        self.workers : dict = resources["Recursos Humanos"]
        '''
    def __str__(self):
        text = f"{self.date}\n"
        for i in self.listEvents:
            text += i.__str__() + "\n"
        return text