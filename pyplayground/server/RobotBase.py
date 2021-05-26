import threading
import socket
import json
import time

class RobotBase():
    """
    Clase base para todos los robots

    Parameters
        name: nombre para el robot
    """

    def __init__( self, name:str ):
        self.me = None
        self.lock = threading.Lock()
        self.enkilock = threading.Lock()
        self.myName = name
        self.myPos = ( 0, 0 )
        self.mySpeed = ( 0, 0 )
        self.myProximitySensorValues = [0]*10
        self.myProximitySensorDistances = [0]*10

    def run( self, conn:socket.socket ):
        """
        Ejecuta para el robot cada comando que va recibiendo
        desde el socket

        Parameters
            conn: el socket a utilizar
        """
        # verifiquemos que no este en ejecucion este robot
        if( not self.lock.acquire( blocking=False ) ): return

        # mis datos como thread
        self.me = threading.current_thread()
        self.me.name = self.me.name + "/" + self.myName

        # aceptamos
        self.running = True
        print( f"Playground >> Robot {self.myName} ejecutando" )
        try:
            # informamos el tipo de robot que somos
            conn.sendall( bytes( self.tipo + "\n", "iso-8859-1" ) )

            # el lector e interprete de los comandos
            while( self.running ):
                try:
                    # leemos el comando y verificamos la conexion
                    cmd = RobotBase.readline( conn )
                    if( cmd == "" ): break

                    # lo procesamos
                    message= json.loads( cmd )
                    if( message["cmd"] == "getSensors" ):
                        resp = self.getSensors()
                    elif( message["cmd"] == "setSpeed" ):
                        resp = self.setSpeed( float( message["leftSpeed"] ), float( message["rightSpeed"] ) )
                    elif( message["cmd"] == "setLedRing" ):
                        resp = self.setLedRing( message["estado"] )
                    elif( message["cmd"] == "setLedsIntensity" ):
                        resp = self.setLedsIntensity( message["leds"] )
                    elif( message["cmd"] == "getCameraImage" ):
                        resp = self.getCameraImage()
                    else:
                        raise Exception( "Comando no reconocido" )

                    # enviamos la respuesta al cliente
                    if( isinstance( resp, dict ) ):
                        resp = json.dumps( resp ) + "\n"
                        resp = bytes( resp, "iso-8859-1" )
                    elif( not isinstance( resp, bytes ) ):
                        raise Exception( "Respuesta debe ser dict o bytes" )
                    conn.sendall( resp )
                except socket.timeout as e:
                    pass
                except Exception as e:
                    print( e )
                    self.running = False
                time.sleep( 0.0001 )
        except:
            pass

        # eso es todo
        print( f"Playground >> Robot {self.myName} finalizado" )
        self.lock.release()

    def finish( self ):
        """
        Finaliza la ejecucion del lector e interprete de comandos del robot
        """
        # debe estar en ejecucion
        while( self.lock.locked() ):
            # cambiamos su variable de control
            self.running = False
            time.sleep( 0.0100 )

    def getSensors( self ) -> dict:
        """
        Obtiene el valor de los sensores del robot

        Return
            Los sensores del robot y sus valores
        """
        self.enkilock.acquire()
        sensors = {
            "pos": self.myPos,
            "speed": self.mySpeed,
            "proximitySensorValues": self.myProximitySensorValues,
            "proximitySensorDistances": self.myProximitySensorDistances
        }
        self.enkilock.release()
        return sensors

    def setSpeed( self, leftSpeed:float, rightSpeed:float ) -> dict:
        """
        Cambia la velocidad de las ruedas del robot

        Parameters
            leftSpeed : valor para la rueda izquierda
            rightSpeed: valor para la rueda derecha
        """
        self.enkilock.acquire()
        self.mySpeed = ( leftSpeed, rightSpeed )
        self.enkilock.release()
        return {}

    def setLedRing( self, on_off:int ) -> dict:
        return {}

    def setLedsIntensity( self, leds:list ) -> dict:
        return {}

    def getCameraImage( self ) -> bytes:
        return int(0).to_bytes( length=4, byteorder="big" )

    def myControlStep( self, dt:float ):
        """Invocada por cada robot"""
        self.enkilock.acquire()
        self.leftSpeed, self.rightSpeed = self.mySpeed
        self.myPos = self.pos
        self.myProximitySensorValues = self.proximitySensorValues
        self.myProximitySensorDistances = self.proximitySensorDistances
        self.enkilock.release()

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
            if( c == b"" ): return ""       # la conexion fue cerrada remotamente
            if( c == b"\n" ): break         # fin de linea
            buff[n] = ord( c )
            n += 1
        return buff[:n].decode( "iso-8859-1" )
