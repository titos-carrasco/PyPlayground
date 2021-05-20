import time
import random
import subprocess

from pyplayground.client import RobotFactory

# THE main
def main():
    # Levantamos el playground en otro procesos
    try:
        pg = subprocess.Popen( [ 'python', 'pyplayground/server/Playground.py', 'worlds/enjambre.world' ], shell=False )
        time.sleep( 1 )
    except Exception as e:
        print( e )
        exit()

    # Los datos de conexion al playground
    host = '127.0.0.1'
    port = 44444

    # Usamos try/except para conocer los errores que se produzcan
    try:
        # Accesamos los robots del enjambre
        robots = []
        for p in range( 44444, 44480 ):  # 44480
            name = f'Thymio-{p}'
            r = RobotFactory.connectRobot( name, host, port )
            robots.append( r)

        # Loop clasico
        while( True ):
            for r in robots:
                r.setSpeed( random.uniform( -1000,1000 ), random.uniform( -1000,1000 ) )
            time.sleep( 2 )
    except ConnectionResetError:
        print( 'Conexion abortada' )
    except Exception as e:
        print( e )

    # Detenemos el playground
    pg.send_signal( subprocess.signal.SIGTERM )


# show time
main()
