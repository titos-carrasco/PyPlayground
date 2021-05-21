"""
Wrapper para el robot del tipo Thymio2

    from pyplayground.client import RobotFactory

    rob = RobotFactory.connectRobot( 'Thymio-01', host, port )
    rob.setSpeed( -1000, 1000 )
    sensores = rob.getSensors()
    rob.setLedIntensity( ( 3:0.5, 5:1.0 } )
"""

import socket

import pyplayground.utils.BasicSockJson as BasicSockJson
import pyplayground.client.RobotBase as RobotBase

class RobotThymio2( RobotBase.RobotBase ):
    def __init__( self, name:str, host:str, port:int, sock:socket.socket ):
        super().__init__( name, host, port, sock )

    def __str__( self ):
        return f'RobotThymio2 >> name:{self.name} - host={self.host} - port={self.port}'

    def setLedsIntensity( self, leds:dict ) -> None:
        """
        Cambia la intensidad de varios LEDs del robot

        Parameters
          leds: Un diccionario con los leds a afectar en su intensidad
                El indice corresponde al número del led
                El valor corresponde a su intensidad (float entre 0 y 1
        """
        pkg = { 'cmd':'setLedsIntensity', 'leds': leds }
        BasicSockJson.send( self.sock, pkg )
        resp = BasicSockJson.read( self.sock, self.buff )['answer']
        return None
