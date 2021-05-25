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
        super().__init__( name )


    def getSensors( self ) -> dict:
        """
        Obtiene el valor de los sensores del robot

        Return
            Los sensores del robot y sus valores
        """
        sensors = super().getSensors()
        sensors["groundSensorValues"] = super().groundSensorValues
        return sensors

    def setLedsIntensity( self, leds:list ) -> dict:
        """
        Cambia la intensidad de los leds del robot

        Parameters
            leds: un arreglo con el valor del tipo float (0 a 1) a
                  asignar como intensidad a cada led. El indice del
                  arreglo corresponde al led a operar
        """
        for idx in range( len(leds) ):
            super().setLedIntensity( idx, leds[idx] )
        return {}
