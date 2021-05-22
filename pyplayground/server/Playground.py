"""
Implementacion de un servidor de robots (playground) utilizando la
la libreria del simulador 2d ENKI de robots

Utiliza un hack para acceder a la libreria pyenki desde Windows y
Linux
"""
import os
import sys
import threading
import socket
import time
import json
import math

#### Inicio del hack
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
#### Inicio del hack

import pyenki
from server.RobotFactory import RobotFactory

class Playground():
    """
    El playground de robots

    Parameters
        world_def: nombre del archivo con la descripcion del playground
                   a construir (debe estar en formato JSON)
    """
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
        self.makeWorld( world_def )

    def run( self ):
        """
        Lanza en ejecución el playground.

        Dada la implementacion de la libreria 'pyenki' este metodo
        no retorna
        """
        #-- QT app debe estar en el thread principal
        self._tDispatcher = threading.Thread( target=self.TDispatcher, args=(), name='TDispatcher' )
        self._tDispatcher.start()
        while ( not self._tRunning ):
            time.sleep( 0.0001 )

        try:
            self.world.runInViewer( ( self.width*0.5, -self.height*0.2 ), self.height*0.9, 0*(math.pi/180.0), -60*(math.pi/180.0) , self.walls )
            #pass
        except Exception as e:
            print( e )
            pass
        print( f'Playground >> Finalizando ...' )
        self.finish()

    def finish( self ):
        """
        Finaliza la ejecucion del playground.

        Este metodo no es utilizado
        """
        if( self._tRunning ):
            self._tRunning = False
            self._tDispatcher.join()
            self._tDispatcher = None
        self.host = None
        self.world = None
        self.robots = None


    def makeWorld( self, fn_world_def:str ):
        """
        Arma el mundo segun la definicion especificada en el archivo

        Este metodo es interno a la clase

        Parameters
            fn_world_def: nombre del archivo con la descripcion del playground
                          a construir (debe estar en formato JSON)
        """
        # lee el archivo de descripcion
        f = open( fn_world_def, 'r' )
        data = f.read()
        world_def = json.loads( data )
        f.close()

        # contruye el playground segun definicion en el archivo
        colors = {}
        for elem in world_def:
            tipo = elem['type']

            # los colores
            if( tipo == 'color' ):
                colors[ elem['name'] ] = pyenki.Color( elem['r']/255., elem['g']/255., elem['b']/255., elem['a']/255. )

            # atributos del mundo
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

            # elementos del mundo
            elif( tipo == 'box' ):
                box = pyenki.RectangularObject( elem['l1'], elem['l2'], elem['height'], elem['mass'], colors[ elem['color'] ] )
                box.pos = ( elem['x'], elem['y'] )
                self.world.addObject( box )
            elif( tipo == 'cylinder' ):
                cyl = pyenki.CircularObject( elem['radius'], elem['height'], elem['mass'], colors[ elem['color'] ] )
                cyl.pos = ( elem['x'], elem['y'] )
                self.world.addObject( cyl )

            # en cuaquier otro caso debe ser un robot
            else:
                name = elem[ 'name' ]
                if( name in self.robots ): raise Exception( f'Robot {name} se encuentra duplicado' )
                rob = RobotFactory.make( tipo, name )
                if( rob is None ): raise Exception( f'Robot {name} no se encuentra definido' )
                rob.pos = ( elem['x'], elem['y'] )
                self.world.addObject( rob )
                self.robots[name] = rob

    def TDispatcher( self ):
        """
        Tarea para despachar las conexiones entrantes desde los clientes

        Este metodo es interno a la clase
        """
        # utiliza un unico socket
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        sock.bind( ( self.host, self.port ) )
        sock.listen( 5 )
        print( f'Playground >> Esperando en tcp://{self.host}:{self.port}' )

        sock.settimeout( 1 )
        self._tRunning = True
        while( self._tRunning ):
            try:
                # recibe las conexiones entrantes
                conn, addr = sock.accept()

                # trata de procesarlas en una tarea especializada
                t = threading.Thread( target=RobotFactory.TRobot, args=( self.robots, conn, addr ), name='TRobot' )
                t.start()
            except socket.timeout as e:
                #print( e )
                pass
            except Exception as e:
                print( e )

        # eso es todo
        sock.shutdown( socket.SHUT_RDWR )
        sock.close()
        sock = None

        for name in self.robots:
            print( f'Playground >> Finalizando robot "{name}"' )
            self.robots[ name ].finish()


#--- show time
if( __name__ == '__main__' ):
    if( len( sys.argv ) == 2 ):
        Playground( sys.argv[1] ).run()
    else:
        Playground( 'example.world' ).run()
