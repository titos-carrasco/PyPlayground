from pyenki import EPuck
from server.RobotBase import RobotBase

class RobotEPuck( RobotBase, EPuck ):
    """
    Clase para interactuar con los robots del tipo EPuck de pyenki
    """

    tipo = "epuck"

    def __init__( self, name ):
        """
        Constructor para robots del tipo "EPuck"

        Parameters
          name: Nombre para el robot
        """
        super().__init__( name )

    def getSensors( self ) -> dict:
        """
        Obtiene el valor de los sensores del robot

        Return
            Los sensores del robot y sus valores
        """
        sensors = super().getSensors()
        return sensors

    def setLedRing( self, on_off:int ) -> dict:
        """
        Apaga o enciende el anillo que rodea al robot

        Parameters
          on_off: 1 para encender, 0 para apagar
        """
        super().setLedRing( on_off )
        return {}

    def getCameraImage( self ) -> bytes:
        """
        Obtiene la imagen de la camara lineal del robot.
        La imagen es de 60x1 pixeles

        Returns
            La magen lineal
        """
        image = bytearray( [ int(v*255) for c in super().cameraImage for v in c.components] )
        data = len(image).to_bytes( length=4, byteorder="big" ) + image
        return data
