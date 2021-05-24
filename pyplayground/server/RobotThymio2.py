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
        sensors = {
            "pos":self.pos,
            "leftSpeed":self.leftSpeed,
            "rightSpeed":self.rightSpeed,
            "proximitySensorValues":self.proximitySensorValues,
            "proximitySensorDistances":self.proximitySensorDistances,
            "groundSensorValues":self.groundSensorValues,
            #"angSpeed":self.angSpeed,
            #"angle":self.angle,
            #"collisionElasticity":self.collisionElasticity,
            #"color":self.color,
            #"dryFrictionCoefficient":self.dryFrictionCoefficient,
            #"height":self.height,
            #"interlacedDistance":self.interlacedDistance,
            #"isCylindric":self.isCylindric,
            #"leftEncoder":self.leftEncoder,
            #"leftOdometry":self.leftOdometry,
            #"mass":self.mass,
            #"momentOfInertia":self.momentOfInertia,
            #"radius":self.radius,
            #"rightEncoder":self.rightEncoder,
            #"rightOdometry":self.rightOdometry,
            #"speed":self.speed,
            #"viscousFrictionCoefficient":self.viscousFrictionCoefficient,
            #"viscousMomentFrictionCoefficient":self.viscousMomentFrictionCoefficient
        }
        return sensors

    def setLedsIntensity( self, leds:list ):
        """
        Cambia la intensidad de los leds del robot

        Parameters
            leds: un arreglo con el valor del tipo float (0 a 1) a
                  asignar como intensidad a cada led. El indice del
                  arreglo corresponde al led a operar
        """
        for idx in range( len(leds) ):
            self.setLedIntensity( idx, leds[idx] )
