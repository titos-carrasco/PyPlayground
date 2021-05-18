import threading
import socket
import time

import utils.BasicSockJson as BasicSockJson


class RobotBase():
    LLEN = 1024

    def __init__( self, name ):
        super().__init__()
        self.name = name
        self._tRobot = None
        self._tRunning = False
        self.sock = None
        self.message = None
        self.hasMessage = False
        self.hasAnswer = False
        self.buff = bytearray( RobotBase.LLEN )

    #--- Levanta el thread de un robot para atender la conexión
    def start( self, sock ):
        if( self._tRunning ): return False
        self.sock = sock
        self._tRobot = threading.Thread( target=self._TRobot, args=(), name=f'TRobot {self.name}' )
        self._tRobot.start()
        while ( not self._tRunning ):
            time.sleep( 0.0001 )
        return True

    #--- Finaliza el thread del robot
    def finish( self ):
        if( self._tRunning ):
            self._tRunning = False
            self._tRobot.join()


    #--- Cambia velocidad de sus ruedas
    def setSpeed( self, leftSpeed, rightSpeed ):
        self.leftSpeed = leftSpeed
        self.rightSpeed = rightSpeed
        return { 'error': '', 'answer':{} }

    #--- Recupera el valor de sus sensores
    def getSensors( self ):
        return { 'error': 'Bad Command', 'answer':{} }

    #--- Privadas

    #--- El interprete de comandos
    def _TRobot( self ):
        print( f'Playground >> Robot {self.name}: Ejecutando' )

        self._tRunning = True
        while( self._tRunning ):
            try:
                self.message = BasicSockJson.read( self.sock, self.buff )
                self.hasMessage = True

                while( not self.hasAnswer ):
                    time.sleep( 0.0001 )
                self.hasAnswer = False

                BasicSockJson.send( self.sock, self.message )
                self.message = None
            except Exception as e:
                print( e )
                self._tRunning = False
                break
            time.sleep( 0.0001 )

        if( not self.sock is None ):
            self.sock.shutdown( socket.SHUT_RDWR )
            self.sock.close()
            self.sock = None
        self._tRobot = None
        self.message = None
        self.hasMessage = False
        self.hasAnswer = False
        print( f'Playground >> Robot {self.name}: Finalizado' )

    #--- Enki loop
    def controlStep( self, dt ):
        if( self.hasMessage ):
            self.hasMessage = False

            if( not 'cmd' in self.message ):
                self.message = { 'error': 'No Command', 'answer':{} }
            elif( self.message['cmd'] == 'getSensors' ):
                self.message = self.getSensors()
            elif( self.message['cmd'] == 'setSpeed' ):
                try:
                    self.message = self.setSpeed( float( self.message['leftSpeed'] ), float( self.message['rightSpeed'] ) )
                except:
                    self.message = { 'error': 'Bad Parameters', 'answer':{} }

            else:
                self.message = { 'error': 'Bad Command', 'answer':{} }

            self.hasAnswer = True
