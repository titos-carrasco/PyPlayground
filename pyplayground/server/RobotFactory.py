import socket
import time

from server.RobotThymio2 import RobotThymio2
from server.RobotEPuck import RobotEPuck

class RobotFactory():
    """
    Clase para fabricar los robots requeridos. Todos sus metodos
    son estaticos
    """

    # construye un robot del tipo especificado
    def make( tipo:str, name:str ) -> object:
        """
        Construye un robot

        Parameters
          tipo: tipo de robot a construir
          name: nombre para el robot

        Return
            Un objeto del tipo de robot solicitado
        """
        if( tipo == "thymio2" ):
            return RobotThymio2( name )
        elif( tipo == "epuck" ):
            return RobotEPuck( name )
        else:
            return None

    def TRobot( robots:dict, conn:socket.socket, addr:tuple ):
        """
        Tarea para controlar un robot del playground. El nombre del
        robot debe ser el primer mensaje enviado por el socket.
        Los parametros conn y addr son el retorno de la invocación
        a socket.accept()

        Parameters
          robots: diccionario con los robots del playground
          conn  : el socket abierto para la comunicacion
          addr  : informacion del punto remoto del socket
        """
        print( f"Playground >> Conexion recibida desde {addr}" )

        name = ""
        try:
            # necesitamos el nombre del robot a utilizar
            conn.settimeout( 2 )
            name = RobotFactory.readline( conn )
            print( f"Playground >> Conectando con robot {name}" )
            # lo ponemos en accion
            if( name in robots ):
                robots[name].run( conn )
        except Exception as e:
            print( e )

        # la tarea finaliza al retornar
        try:
            conn.shutdown( socket.SHUT_RDWR )
            conn.close()
        except:
            pass
        conn = None
        print( f"Playground >> Conexion finalizada para {addr}" )

    # permite leer una linea desde el socket
    def readline( conn:socket.socket ) -> str:
        """
        Lee una linea desde el socket.

        Este metodo es interno a la clase

        Parameters
            conn: el socket desde el cual leer

        Return
            La linea leida
        """
        ll = 64
        buff = bytearray( ll )
        n = 0
        while( n < ll ):
            c = conn.recv(1)
            if( c == b"" ): break           # el socket fue cerrado remotamente
            if( c == b"\n" ): break         # fin de linea
            buff[n] = ord( c )
            n += 1
        return buff[:n].decode( "iso-8859-1" )
