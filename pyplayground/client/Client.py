import os
import sys
import socket

import pyplayground.utils.BasicSockJson as BasicSockJson


#--- Public Class
class RobotControl():
    LLEN = 1024

    # constructor
    def __init__( self, name, host, port, sock ):
        self.name = name
        self.host = host
        self.port = port
        self.sock = sock
        self.buff = bytearray( RobotControl.LLEN )

    # public
    def close( self ):
        if( self.sock is None ): return
        self.sock.shutdown( socket.SHUT_RDWR )
        self.sock.close()
        self.name = None
        self.host = None
        self.port = None
        self.sock = None
        self.buff = None

    def getName( self ):
        return self.name

    def setSpeed( self, left, right ):
        pkg = { 'cmd':'setSpeed', 'leftSpeed': left, 'rightSpeed': right }
        BasicSockJson.send( self.sock, pkg )
        resp = BasicSockJson.read( self.sock, self.buff )['answer']
        return resp

    def getSensors( self ):
        pkg = { 'cmd':'getSensors' }
        BasicSockJson.send( self.sock, pkg )
        resp = BasicSockJson.read( self.sock, self.buff )['answer']['sensors']
        return resp

    def __str__( self ):
        return f'RobotControl >> name:{self.name} - host={self.host} - port={self.port}'

    # static & public
    def connect( name, host, port ):
        if( host == '' ): host = '0.0.0.0'
        try:
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            sock.connect( ( host, port ) )

            pkg = { 'cmd':'connect', 'name': name }
            BasicSockJson.send( sock, pkg )

            buff = bytearray( RobotControl.LLEN )
            resp = BasicSockJson.read( sock, buff )['answer']
            buff = None

            if( resp['type'] == 'thymio2' ):
                return RobotThymio2( name, host, port, sock )
            elif( resp['type'] == 'epuck' ):
                return RobotEPuck( name, host, port, sock )
            else:
                raise KeyError
        except Exception as e:
            print( e )
            sock.shutdown( socket.SHUT_RDWR )
            sock.close()
            raise


#-- package visibility
class RobotEPuck( RobotControl ):
    # constructor
    def __init__( self, name, host, port, sock ):
        super().__init__( name, host, port, sock )

    def __str__( self ):
        return f'RobotEnki >> name:{self.name} - host={self.host} - port={self.port}'


#-- private inner class
class RobotThymio2( RobotControl ):
    # constructor
    def __init__( self, name, host, port, sock ):
        super().__init__( name, host, port, sock )

    def __str__( self ):
        return f'RobotThymio2 >> name:{self.name} - host={self.host} - port={self.port}'
