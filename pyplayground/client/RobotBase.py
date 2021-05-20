import socket

import pyplayground.utils.BasicSockJson as BasicSockJson

class RobotBase():
    LLEN = 512*3

    def __init__( self, name:str, host:str, port:int, sock:socket.socket ) -> None:
        self.name = name
        self.host = host
        self.port = port
        self.sock = sock
        self.buff = bytearray( RobotBase.LLEN )

    def close( self ) -> None:
        if( self.sock is None ): return
        self.sock.shutdown( socket.SHUT_RDWR )
        self.sock.close()
        self.name = None
        self.host = None
        self.port = None
        self.sock = None
        self.buff = None

    def getName( self ) -> str:
        return self.name

    def setSpeed( self, left:int, right:int ) -> None:
        pkg = { 'cmd':'setSpeed', 'leftSpeed': left, 'rightSpeed': right }
        BasicSockJson.send( self.sock, pkg )
        resp = BasicSockJson.read( self.sock, self.buff )['answer']
        return None

    def getSensors( self ) -> dict :
        pkg = { 'cmd':'getSensors' }
        BasicSockJson.send( self.sock, pkg )
        resp = BasicSockJson.read( self.sock, self.buff )['answer']['sensors']
        return resp

    def setLedRing( self, on_off:bool ) -> None:
        return None

    def setLedsIntensity( self, leds:dict ) -> None:
        return None

    def getCameraImage( self ) -> None:
        return None

    def __str__( self ):
        return f'RobotControl >> name:{self.name} - host={self.host} - port={self.port}'
