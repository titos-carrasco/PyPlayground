import os
import sys
import threading
import socket
import time
import json
import math

# Not the best way
pkgpath = os.path.dirname( os.path.abspath( f'{__file__}' ) )
if( pkgpath in sys.path ):
    sys.path.remove( pkgpath )
pkgpath = os.path.dirname( os.path.abspath( f'{__file__}/..' ) )
sys.path.insert( 0, pkgpath )

# Windows
if( os.name == 'nt' ):
    cwd = os.getcwd()
    os.add_dll_directory( f'{pkgpath}\\server\\windows\\dll' )
    os.environ['QT_PLUGIN_PATH'] =  f'{pkgpath}\\server\\windows\\qt'
    os.environ['QT_OPENGL'] = 'desktop'
    sys.path.append( f'{pkgpath}/server/windows' )
# Linux
else:
    sys.path.append( f'{pkgpath}/server/linux' )

import pyenki
import server.RobotFactory as RobotFactory
import utils.BasicSockJson as BasicSockJson

class Playground():
    #--- Constructor
    def __init__( self, world_def  ):
        self.host = None
        self.port = None
        self.world = None
        self.width = 0
        self.height = 0
        self.walls = 0
        self.robots = {}
        self._tDispatcher = None
        self._tRunning = False
        self._makeWorld( world_def )

    #-- QT app debe estar en el thread principal
    def run( self ):
        self._tDispatcher = threading.Thread( target=self._TDispatcher, args=(), name='TDispatcher' )
        self._tDispatcher.start()
        while ( not self._tRunning ):
            time.sleep( 0.0001 )

        try:
            self.world.runInViewer( ( self.width*0.5, -self.height*0.2 ), self.height*0.9, 0*(math.pi/180.0), -60*(math.pi/180.0) , self.walls )
            #pass
        except Exception as e:
            print( e )
            pass
        self.finish()

    def finish( self ):
        if( self._tRunning ):
            self._tRunning = False
            self._tDispatcher.join()
            self._tDispatcher = None
        self.host = None
        self.world = None
        self.robots = None

    #--- Privadas

    #--- Arma el mundo segun la definicion especificada en el archivo
    def _makeWorld( self, fn_world_def ):
        f = open( fn_world_def, 'r' )
        data = f.read()
        world_def = json.loads( data )
        f.close()

        colors = {}
        for elem in world_def:
            tipo = elem['type']

            #--- Un color
            if( tipo == 'color' ):
                colors[ elem['name'] ] = pyenki.Color( elem['r']/255., elem['g']/255., elem['b']/255., elem['a']/255. )

            #--- El mundo
            elif( tipo == 'world' ):
                if( elem['width'] == 0 or elem['height'] == 0 ):
                    self.width = 100
                    self.height = 100
                else:
                    self.width = elem['width']
                    self.height = elem['height']
                self.walls = elem['walls']
                if( elem['ground'] == '' ):
                    self.world = pyenki.World( self.width, self.height, colors[ elem['color'] ] )
                else:
                    ground = os.path.dirname( fn_world_def ) + '/' + elem['ground']
                    self.world = pyenki.WorldWithTexturedGround( self.width, self.height, ground, colors[ elem['color'] ] )
                self.host = elem['host'] if elem['host'] != '' else '0.0.0.0'
                self.port = elem['port']

            #--- Un elemento en el mundo
            elif( tipo == 'box' ):
                box = pyenki.RectangularObject( elem['l1'], elem['l2'], elem['height'], elem['mass'], colors[ elem['color'] ] )
                box.pos = ( elem['x'], elem['y'] )
                self.world.addObject( box )
            elif( tipo == 'cylinder' ):
                cyl = pyenki.CircularObject( elem['radius'], elem['height'], elem['mass'], colors[ elem['color'] ] )
                cyl.pos = ( elem['x'], elem['y'] )
                self.world.addObject( cyl )

            #--- En cuaquier otro caso debe ser un robot
            else:
                name = elem[ 'name' ]
                if( name in self.robots ): raise Exception( f'Robot {name} se encuentra duplicado' )
                rob = RobotFactory.makeRobot( tipo, name )
                if( rob is None ): raise Exception( f'Robot {name} no se encuentra definido' )
                rob.pos = ( elem['x'], elem['y'] )
                self.world.addObject( rob )
                self.robots[name] = rob

    #-- El despachador de conexiones entrantes
    def _TDispatcher( self ):
        LLEN = 512*3
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        sock.bind( ( self.host, self.port ) )
        sock.listen( len( self.robots ) )
        #sock.setblocking( 0 )
        buff = bytearray( LLEN )
        print( f'Playground >> Esperando en tcp://{self.host}:{self.port}' )

        self._tRunning = True
        while( self._tRunning ):
            try:
                conn, addr = sock.accept()
                print( f'Playground >> Conexion iniciada desde {addr}' )

                msg = BasicSockJson.read( conn, buff )
                if( ( 'cmd' in msg and msg['cmd'] == 'connect' ) and ( 'name' in msg and msg['name'] in self.robots ) ):
                    rob = self.robots[ msg['name'] ]
                    if( rob.start( conn ) ):
                        BasicSockJson.send( conn, { 'error':'', 'answer':{ "type":rob.tipo } } )
                    else:
                        BasicSockJson.send( conn, { 'error':'Robot already running', 'answer':{} } )
                        raise KeyError
                else:
                    BasicSockJson.send( conn, { 'error':'Bad Packet', 'answer':{} } )
                    raise KeyError
            except BlockingIOError:
                pass
            except Exception as e:
                conn.shutdown( socket.SHUT_RDWR )
                conn.close()
                print( f'Playground >> Conexion rechazada' )

        sock.shutdown( socket.SHUT_RDWR )
        sock.close()
        sock = None

        for robot_name in self.robots:
            self.robots[ robot_name ].finish()


#--- show time
if( __name__ == '__main__' ):
    if( len( sys.argv ) == 2 ):
        Playground( sys.argv[1] ).run()
    else:
        Playground( 'example.world' ).run()
