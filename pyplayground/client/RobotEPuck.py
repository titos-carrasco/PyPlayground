"""
Wrapper para el robot del tipo EPuck

    from pyplayground.client import RobotFactory

    rob = RobotFactory.connectRobot( 'Epuck-01', host, port )
    rob.setSpeed( -1000, 1000 )
    sensores = rob.getSensors()
    rob.setLedRing( True )
    image = rob.getCameraImage()
"""
import socket

import pyplayground.utils.BasicSockJson as BasicSockJson
import pyplayground.client.RobotBase as RobotBase

class RobotEPuck( RobotBase.RobotBase ):
    def __init__( self, name:str, host:str, port:int, sock:socket.socket ):
        super().__init__( name, host, port, sock )

    def __str__( self ):
        return f'RobotEnki >> name:{self.name} - host={self.host} - port={self.port}'

    def setLedRing( self, on_off:bool ) -> None:
        """
        apaga o enciende el anillo que rodea al robot

        Parameters
          on_off: True enciende el anillo, False lo apaga

        """
        led_on = 1 if on_off else 0
        pkg = { 'cmd':'setLedRing', 'estado': on_off }
        BasicSockJson.send( self.sock, pkg )
        resp = BasicSockJson.read( self.sock, self.buff )['answer']
        return None

    def getCameraImage( self ) -> list :
        """
        Obtiene la imagen de la camara lineal del robot

        Return
            una lista con los puntos de la imagen (60 de ancho x 1 de alto)
        """
        pkg = { 'cmd':'getCameraImage' }
        BasicSockJson.send( self.sock, pkg )
        resp = BasicSockJson.read( self.sock, self.buff )['answer']['image']
        resp = bytearray( resp, 'iso-8859-1' )
        l = len( resp )
        resp = [ tuple( resp[i:i+4] ) for i in range( 0, l, 4 ) ]
        return resp
