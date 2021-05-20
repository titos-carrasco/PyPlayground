import time
import random
import subprocess

from pyplayground.client import RobotFactory
import pygame

# THE main
def main():
    # Levantamos el playground en otro procesos
    try:
        pg = subprocess.Popen( [ 'python', 'pyplayground/server/Playground.py', 'worlds/epuck.world' ], shell=False )
        time.sleep( 1 )
    except Exception as e:
        print( e )
        exit()

    # Los datos de conexion al playground
    host = '127.0.0.1'
    port = 44444

    # Usamos try/except para conocer los errores que se produzcan
    try:
        # Accesamos el robot y configuramos algunos de sus atributos
        epuck  = RobotFactory.connectRobot( 'Epuck-01' , host, port )
        epuck.setLedRing( True )
        epuck.setSpeed( -10, 10 )

        # Obtenemos la primera imagen
        img = epuck.getCameraImage()
        imglen = len( img )

        # Usaremos "pygame" para mostrar la camara lineal del robot
        pygame.init()
        screen = pygame.display.set_mode( ( imglen*10, 80) )

        # Loop clasico
        while( True ):
            # trazamos la imagen de la camara
            for i in range( imglen ):
                color = img[ i ]
                pygame.draw.rect( screen, color, ( i*10, 0, 10, 80) )
            pygame.display.flip()

            # obtenemos la siguiente imagen
            img = epuck.getCameraImage()
            time.sleep( 0.001 )
    except ConnectionResetError:
        print( 'Conexion abortada' )
    except Exception as e:
        print( e )

    # Detenemos el playground
    pg.send_signal( subprocess.signal.SIGTERM )


# show time
main()
