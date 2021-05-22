import socket
import json

class RobotBase():
    """
    Clase base de los robots

    Parameters
        name: nombre del robot a controlar en el playground
        host: servidor en donde se encuenra este robot
        port: puerta en donde se encuentra este robot
        sock: socket para comunicarse con el robot remoto
    """

    def __init__( self, name:str, host:str, port:int, sock:socket.socket ):
        self.name = name
        self.host = host
        self.port = port
        self.sock = sock
        self.buff = bytearray( 512*3 )

    def close( self ):
        """
        Cierra la conexion con el robot
        """
        if( self.sock is None ): return
        self.sock.shutdown( socket.SHUT_RDWR )
        self.sock.close()
        self.name = None
        self.host = None
        self.port = None
        self.sock = None
        self.buff = None

    def getName( self ) -> str:
        """
        Obtiene el nombre del robot

        Return
            El nombre del robot
        """
        return self.name

    def setSpeed( self, left:int, right:int ) -> None:
        """
        Cambia la velocidad de las ruedas del robot

        Parameters
            leftSpeed : valor para la rueda izquierda
            rightSpeed: valor para la rueda derecha
        """
        pkg = { 'cmd':'setSpeed', 'leftSpeed': left, 'rightSpeed': right }
        resp = self.sendPkg( pkg )

    def getSensors( self ) -> dict :
        """
        Obtiene el valor de los sensores del robot

        Return
            Los sensores del robot y sus valores
        """
        pkg = { 'cmd':'getSensors' }
        resp = self.sendPkg( pkg )
        return resp

    def sendPkg( self, pkg:dict ) -> object:
        self.sock.sendall( bytearray( json.dumps( pkg ) + '\n', 'iso-8859-1' ) )
        resp = self.readline()
        return json.loads( resp )


    def readline( self ) -> str:
        """
        Lee una linea desde el socket

        Este metodo es interno a la clase

        Parameters
            conn: el socket desde el cual leer

        Return
            La linea leida
        """
        ll = len( self.buff )
        n = 0
        while( n < ll ):
            c = self.sock.recv(1)
            if( c == b'' ): return ''       # la conexion fue cerrada remotamente
            if( c == b'\n' ): break         # fin de linea
            self.buff[n] = ord( c )
            n += 1
        return self.buff[:n].decode( 'iso-8859-1' )

    def __str__( self ):
        return f'RobotControl >> name:{self.name} - host={self.host} - port={self.port}'
