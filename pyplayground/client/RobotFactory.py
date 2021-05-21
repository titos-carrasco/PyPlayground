"""
Fabrica de conexiones a los robots
---

    from pyplayground.client import RobotFactory

    rob = RobotFactory.connectRobot( 'Thymio-01', '127.0.0.1', 44444 )
"""
import socket

import pyplayground.utils.BasicSockJson as BasicSockJson
import pyplayground.client.RobotThymio2 as RobotThymio2
import pyplayground.client.RobotEPuck as RobotEPuck

def connectRobot( name:str, host:str, port:int ) -> object:
    """
    Conecta localmente con un robot remoto

    Parameters
      name: Nombre del robot a conectar
      host: Servidor en donde se encuentra el robot
      port: Puerta en donde escucha el robot

    Return
        Objeto del tipo 'RobotThymio2' o 'RobotEPuck' segun
        sea el tipo de robot conectado

    Forma de uso
        from pyplayground.client import RobotFactory

        rob = RobotFactory.connectRobot( 'Thymio-01', '127.0.0.1', 44444 )
    """
    LLEN = 512*3
    if( host == '' ): host = '0.0.0.0'
    try:
        # Nos conectamos al servidor
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        sock.connect( ( host, port ) )

        # Le pedimos una conexion al robot
        pkg = { 'cmd':'connect', 'name': name }
        BasicSockJson.send( sock, pkg )

        # Recibimos la respuesta del servidor
        buff = bytearray( LLEN )
        resp = BasicSockJson.read( sock, buff )['answer']
        buff = None

        # Retornamos el robot segun su tipo
        if( resp['type'] == 'thymio2' ):
            return RobotThymio2.RobotThymio2( name, host, port, sock )
        elif( resp['type'] == 'epuck' ):
            return RobotEPuck.RobotEPuck( name, host, port, sock )
        else:
            raise KeyError
    except Exception as e:
        print( e )
        sock.shutdown( socket.SHUT_RDWR )
        sock.close()
        raise
