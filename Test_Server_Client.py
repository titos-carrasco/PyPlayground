import time
import random
import subprocess

from pyplayground.client import RobotFactory

# THE main
def main():
    # Levantamos el playground en otro proceso
    try:
        pg = subprocess.Popen( [ 'python', 'pyplayground/server/Playground.py', 'worlds/simple.world' ], shell=False )
        time.sleep( 1 )
    except Exception as e:
        print( e )
        exit()

    # Los datos de conexion al playground
    host = '127.0.0.1'
    port = 44444

    # Usamos try/except para conocer los errores que se produzcan
    try:
        # Accesamos los robots
        rob01 = RobotFactory.connectRobot( 'Thymio-01', host, port )
        rob02 = RobotFactory.connectRobot( 'Epuck-01', host, port )

        # Loop clasico
        while( True ):
            rob01.setSpeed( random.uniform(-100,100), random.uniform(-100,100) )
            rob02.setSpeed( random.uniform(-100,1000), random.uniform(-100,100) )

            s01 = rob01.getSensors()
            s02 = rob02.getSensors()

            time.sleep( 1 )
    except ConnectionResetError:
        print( 'Conexion abortada' )
    except Exception as e:
        print( e )

    # Detenemos el playground
    pg.send_signal( subprocess.signal.SIGTERM )


# show time
main()
