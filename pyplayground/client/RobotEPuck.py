import socket

import pyplayground.utils.BasicSockJson as BasicSockJson
import pyplayground.client.RobotBase as RobotBase

class RobotEPuck( RobotBase.RobotBase ):
    def __init__( self, name:str, host:str, port:int, sock:socket.socket ):
        super().__init__( name, host, port, sock )

    def __str__( self ):
        return f'RobotEnki >> name:{self.name} - host={self.host} - port={self.port}'

    def setLedRing( self, on_off:bool ) -> None:
        led_on = 1 if on_off else 0
        pkg = { 'cmd':'setLedRing', 'estado': on_off }
        BasicSockJson.send( self.sock, pkg )
        resp = BasicSockJson.read( self.sock, self.buff )['answer']
        return None

    def getCameraImage( self ) -> list :
        pkg = { 'cmd':'getCameraImage' }
        BasicSockJson.send( self.sock, pkg )
        resp = BasicSockJson.read( self.sock, self.buff )['answer']['image']
        resp = bytearray( resp, 'iso-8859-1' )
        l = len( resp )
        resp = [ tuple( resp[i:i+4] ) for i in range( 0, l, 4 ) ]
        return resp
