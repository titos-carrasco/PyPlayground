import socket

from pyplayground.client.RobotThymio2 import RobotThymio2
from pyplayground.client.RobotEPuck import RobotEPuck

class RobotFactory():
    """
    Fabrica de robots. Todos sus metodos son estaticos
    """

    def connect( name:str, host:str, port:int ) -> object:
        """
        Conecta a un robot de un playground remoto

        Parameters
          name: Nombre del robot a conectar
          host: Servidor en donde se encuentra el playground
          port: Puerta en donde escucha el playground

        Return
            Objeto del tipo de robot a controlar
        """
        if( host == '' ): host = '0.0.0.0'
        try:
            # nos conectamos al servidor
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            sock.connect( ( host, port ) )

            # pedimos conexion al robot
            sock.sendall( bytearray( name + '\n', 'iso-8859-1' ) )

            # recibimos la respuesta del servidor
            tipo = RobotFactory.readline( sock )

            # generamos el robot segun su tipo
            if( tipo == 'thymio2' ):
                return RobotThymio2( name, host, port, sock )
            elif( tipo == 'epuck' ):
                return RobotEPuck( name, host, port, sock )
            elif( tipo == '' ):
                raise Exception( f"Robot '{name}' conectado a otro cliente" )
            else:
                raise Exception( 'Tipo de Robot no implementado' )
        except Exception as e:
            sock.shutdown( socket.SHUT_RDWR )
            sock.close()
            raise

    def readline( conn:socket.socket ) -> str:
        """
        Lee una linea desde el socket

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
            if( c == b'' ): return ''       # la conexion fue cerrada remotamente
            if( c == b'\n' ): break         # fin de linea
            buff[n] = ord( c )
            n += 1
        return buff[:n].decode( 'iso-8859-1' )
