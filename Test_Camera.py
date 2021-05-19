import time
import random
import subprocess

from pyplayground.client import Client
import pygame

def main():
    # Server
    try:
        pg = subprocess.Popen( [ 'python', 'pyplayground/server/Playground.py', 'worlds/epuck.world' ], shell=False )
        time.sleep( 1 )
    except Exception as e:
        print( e )
        exit()

    # Client
    host = '127.0.0.1'
    port = 44444
    try:
        epuck  = Client.RobotControl.connect( 'Epuck-01' , host, port )
        epuck.setLedRing( True )
        epuck.setSpeed( -1, 1 )
        img = epuck.getCameraImage()
        imglen = len( img )

        pygame.init()
        screen = pygame.display.set_mode( ( imglen*10, 80) )
        while( True ):
            for i in range( imglen ):
                color = img[ i ]
                pygame.draw.rect( screen, color, ( i*10, 0, 10, 80) )
            pygame.display.flip()

            img = epuck.getCameraImage()
            time.sleep( 0.001 )
    except ConnectionResetError:
        print( 'Conexion abortada' )
    except Exception as e:
        print( e )

    # Server shutdown
    pg.send_signal( subprocess.signal.SIGTERM )


# show time
main()
