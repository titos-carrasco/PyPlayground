import socket

import pyplayground.utils.BasicSockJson as BasicSockJson
import pyplayground.client.RobotBase as RobotBase

class RobotThymio2( RobotBase.RobotBase ):
    def __init__( self, name:str, host:str, port:int, sock:socket.socket ):
        super().__init__( name, host, port, sock )

    def __str__( self ):
        return f'RobotThymio2 >> name:{self.name} - host={self.host} - port={self.port}'

    def setLedsIntensity( self, leds:dict ) -> None:
        pkg = { 'cmd':'setLedsIntensity', 'leds': leds }
        BasicSockJson.send( self.sock, pkg )
        resp = BasicSockJson.read( self.sock, self.buff )['answer']
        return None
