import socket

import pyplayground.utils.BasicSockJson as BasicSockJson
import pyplayground.client.RobotThymio2 as RobotThymio2
import pyplayground.client.RobotEPuck as RobotEPuck

def connectRobot( name:str, host:str, port:int ):
    LLEN = 512*3
    if( host == '' ): host = '0.0.0.0'
    try:
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        sock.connect( ( host, port ) )

        pkg = { 'cmd':'connect', 'name': name }
        BasicSockJson.send( sock, pkg )

        buff = bytearray( LLEN )
        resp = BasicSockJson.read( sock, buff )['answer']
        buff = None
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
