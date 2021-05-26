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
        RobotBase.__init__( self, name )
        EPuck.__init__( self )
        self.myLedRing = 0
        self.myCameraImage = None

    def setLedRing( self, on_off:int ) -> dict:
        """
        Apaga o enciende el anillo que rodea al robot

        Parameters
          on_off: 1 para encender, 0 para apagar
        """
        self.enkilock.acquire()
        self.myLedRing = on_off
        self.enkilock.release()
        return {}

    def getCameraImage( self ) -> bytes:
        """
        Obtiene la imagen de la camara lineal del robot.
        La imagen es de 60x1 pixeles

        Returns
            La magen lineal
        """
        self.enkilock.acquire()
        image = self.myCameraImage
        self.enkilock.release()

        image = bytes( [ int(v*255) for c in image for v in c.components] )
        data = len(image).to_bytes( length=4, byteorder="big" ) + image
        return data

    def controlStep( self, dt:float ):
        """Invocada desde la libreria "pyenki" para cada robot"""
        self.myControlStep( dt )
        self.enkilock.acquire()
        self.myCameraImage = self.cameraImage
        EPuck.setLedRing( self, self.myLedRing )
        self.enkilock.release()
