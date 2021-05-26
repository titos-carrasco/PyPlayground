from pyenki import Thymio2
from server.RobotBase import RobotBase

class RobotThymio2( RobotBase, Thymio2 ):
    """
    Clase para interactuar con los robots del tipo Thymio2 del pyenki

    Parameters
      name: nombre para el robot
    """

    tipo = "thymio2"

    def __init__( self, name:str ):
        RobotBase.__init__( self, name )
        Thymio2.__init__( self )

        self.myLeds= [0]*23
        self.myGroundSensorValues = [0]*2

    def getSensors( self ) -> dict:
        """
        Obtiene el valor de los sensores del robot

        Return
            Los sensores del robot y sus valores
        """
        sensors = super().getSensors()
        self.enkilock.acquire()
        sensors["groundSensorValues"] = self.myGroundSensorValues
        self.enkilock.release()
        return sensors

    def setLedsIntensity( self, leds:list ) -> dict:
        """
        Cambia la intensidad de los leds del robot

        Parameters
            leds: un arreglo con el valor del tipo float (0 a 1) a
                  asignar como intensidad a cada led. El indice del
                  arreglo corresponde al led a operar
        """
        self.enkilock.acquire()
        self.myLeds = leds
        self.enkilock.release()
        return {}

    def controlStep( self, dt:float ):
        """Invocada desde la libreria "pyenki" para cada robot"""
        self.myControlStep( dt )
        self.enkilock.acquire()
        self.myGroundSensorValues = super().groundSensorValues
        for idx in range( len( self.myLeds ) ):
            self.setLedIntensity( idx, self.myLeds[idx] )
        self.enkilock.release()
