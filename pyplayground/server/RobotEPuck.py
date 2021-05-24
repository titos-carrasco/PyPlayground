from pyenki import EPuck
from server.RobotBase import RobotBase

class RobotEPuck( RobotBase, EPuck ):
    """
    Clase para interactuar con los robots del tipo EPuck de pyenki
    """

    tipo = "epuck"

    #--- Constructor
    def __init__( self, name ):
        """
        Constructor para robots del tipo "EPuck"

        Parameters
          name: Nombre para el robot
        """
        super().__init__( name )

    #--- Retorna un diccionario con el valor de sus sensores
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
            "proximitySensorDistances":self.proximitySensorDistances,
            "proximitySensorValues":self.proximitySensorValues,
            #"angSpeed":self.angSpeed,
            #"angle":self.angle,
            #"cameraImage":self.cameraImage,
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

    def setLedRing( self, on_off:int ):
        """
        Apaga o enciende el anillo que rodea al robot

        Parameters
          on_off: 1 para encender, 0 para apagar
        """
        super().setLedRing( on_off )

    def getCameraImage( self ) -> bytearray:
        """
        Obtiene la imagen de la camara lineal del robot.
        La imagen es de 60x1 pixeles

        Returns
            La magen lineal
        """
        image = bytearray( [ int(v*255) for c in self.cameraImage for v in c.components] ).decode( "iso-8859-1" )
        return image
