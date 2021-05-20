import time
import random
import subprocess

from pyplayground.client import RobotFactory

# THE main
def main():
    # Levantamos el playground en otro procesos
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
        # Accesamos los robots y configuramos algunos de sus atributos
        thymio = RobotFactory.connectRobot( 'Thymio-01', host, port )
        epuck  = RobotFactory.connectRobot( 'Epuck-01' , host, port )
        epuck.setLedRing( True )

        ledval = 0.5
        t = 0

        # Loop clasico
        while( True ):
            if( time.time() - t > 1 ):
                dicc = {}
                for i in range(3,23): dicc[ i ] = ledval
                thymio.setLedsIntensity( dicc )
                ledval = 0.5 if ledval == 0 else 0
                t = time.time()
            time.sleep( 0.001 )
    except ConnectionResetError:
        print( 'Conexion abortada' )
    except Exception as e:
        print( e )

    # Detenemos el playground
    pg.send_signal( subprocess.signal.SIGTERM )


# show time
main()
