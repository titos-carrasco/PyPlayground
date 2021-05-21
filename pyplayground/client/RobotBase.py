"""
Clase base de los robots
"""
import socket

import pyplayground.utils.BasicSockJson as BasicSockJson

class RobotBase():
    """
    Parameters
      name: Nombre del robot a conectar
      host: Servidor en donde se encuentra el robot
      port: Puerta en donde escucha el robot
      sock: Socket en donde esta conectado el robot
    """
    LLEN = 512*3

    def __init__( self, name:str, host:str, port:int, sock:socket.socket ) -> None:
        self.name = name
        self.host = host
        self.port = port
        self.sock = sock
        self.buff = bytearray( RobotBase.LLEN )

    def close( self ) -> None:
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
        Retorna el nombre del robot

        Return
            El nombre del robot
        """
        return self.name

    def setSpeed( self, left:int, right:int ) -> None:
        """
        Cambia la velocidad de los motores de las ruedas del robot'

        Parameters
          left : intensidad rueda izquierda (-1000 a 1000)
          right: intensidad rueda derecha (-1000 a 1000)
        """
        pkg = { 'cmd':'setSpeed', 'leftSpeed': left, 'rightSpeed': right }
        BasicSockJson.send( self.sock, pkg )
        resp = BasicSockJson.read( self.sock, self.buff )['answer']
        return None

    def getSensors( self ) -> dict :
        """
        Obtiene el valor de todos los sensores del robot

        Return
            Un diccionario con el valor de los sensores
        """
        pkg = { 'cmd':'getSensors' }
        BasicSockJson.send( self.sock, pkg )
        resp = BasicSockJson.read( self.sock, self.buff )['answer']['sensors']
        return resp

    def __str__( self ):
        return f'RobotControl >> name:{self.name} - host={self.host} - port={self.port}'
