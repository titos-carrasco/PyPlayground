import threading
import socket
import select
import json
import time

class RobotBase():
    """
    Clase base para todos los robots

    Parameters
        name: nombre para el robot
    """

    def __init__( self, name:str ):
        super().__init__()
        self.name = name
        self.lock = threading.Lock()
        self.message = None
        self.hasMessage = False
        self.hasAnswer = False
        self.running = False

    def run( self, conn:socket.socket ):
        """
        Ejecuta para el robot cada comando que va recibiendo
        desde el socket

        Parameters
            conn: el socket a utilizar
        """
        # verifiquemos que no este en ejecucion este robot
        if( not self.lock.acquire( blocking=False ) ): return

        # aceptamos
        self.running = True
        print( f'Playground >> Robot {self.name} ejecutando' )
        try:
            # informamos el tipo de robot que somos
            conn.sendall( bytearray( self.tipo + '\n', 'iso-8859-1' ) )

            # el lector e interprete de los comandos
            while( self.running ):
                try:
                    # leemos el comando y verificamos la conexion
                    cmd = RobotBase.readline( conn )
                    if( cmd == '' ): break

                    # lo preparamos para que sea procesado en el loop de enki
                    self.message = json.loads( cmd )
                    self.hasMessage = True

                    # esperamos a que haya sido procesado en el loop de enki
                    while( not self.hasAnswer ):
                        time.sleep( 0.0001 )
                    self.hasAnswer = False

                    # enviamos la respuesta al cliente
                    resp = json.dumps( self.message ) + '\n'
                    resp = bytearray( resp, 'iso-8859-1' )
                    conn.sendall( resp )
                    self.message = None
                except socket.timeout as e:
                    pass
                except Exception as e:
                    self.running = False
                time.sleep( 0.0001 )
        except:
            pass

        # eso es todo
        print( f'Playground >> Robot {self.name} finalizado' )
        self.message = None
        self.hasMessage = False
        self.hasAnswer = False
        self.lock.release()

    def finish( self ):
        """
        Finaliza la ejecucion del lector e interprete de comandos del robot
        """
        # debe estar en ejecunion
        while( self.lock.locked() ):
            # cambiamos su variable de control
            self.running = False
            time.sleep( 0.0001 )

    def setSpeed( self, leftSpeed:int, rightSpeed:int ):
        """
        Cambia la velocidad de las ruedas del robot

        Parameters
            leftSpeed : valor para la rueda izquierda
            rightSpeed: valor para la rueda derecha
        """
        self.leftSpeed = leftSpeed
        self.rightSpeed = rightSpeed
        return None


    #--- Enki loop
    def controlStep( self, dt:float ):
        """
        Invocada desde la libreria 'pyenki' para cada robot

        Este metodo es interno a la clase

        Parameters
            dt: ???
        """
        # procesamos el mensaje recibido en el metodo run()
        if( self.hasMessage ):
            self.hasMessage = False

            try:
                if( self.message['cmd'] == 'getSensors' ):
                    self.message = self.getSensors()
                elif( self.message['cmd'] == 'setSpeed' ):
                    self.message = self.setSpeed( float( self.message['leftSpeed'] ), float( self.message['rightSpeed'] ) )
                elif( self.message['cmd'] == 'setLedRing' ):
                    self.message = self.setLedRing( self.message['estado'] )
                elif( self.message['cmd'] == 'setLedsIntensity' ):
                    self.message = self.setLedsIntensity( self.message['leds'] )
                elif( self.message['cmd'] == 'getCameraImage' ):
                    self.message = self.getCameraImage()
                else:
                    raise KeyError
            except Exception as e:
                print( e )
                self.message = None

            self.hasAnswer = True
            time.sleep( 0.0001 )

    def readline( conn:socket.socket ) -> str:
        """
        Lee una linea desde el socket

        Este metodo es interno a la clase

        Parameters
            conn: el socket desde el cual leer

        Return
            La linea leida
        """
        ll = 256
        buff = bytearray( ll )
        n = 0
        while( n < ll ):
            c = conn.recv(1)
            if( c == b'' ): return ''       # la conexion fue cerrada remotamente
            if( c == b'\n' ): break         # fin de linea
            buff[n] = ord( c )
            n += 1
        return buff[:n].decode( 'iso-8859-1' )
