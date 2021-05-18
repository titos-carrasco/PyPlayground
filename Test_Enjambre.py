import time
import random
import subprocess

from pyplayground.client import Client


#---
def main():
    # Server
    try:
        pg = subprocess.Popen( [ 'python', 'pyplayground/server/Playground.py', 'worlds/enjambre.world' ], shell=False )
        time.sleep( 1 )
    except Exception as e:
        print( e )
        exit()

    # Client
    host = '127.0.0.1'
    port = 44444
    try:
        robots = []
        for p in range( 44444, 44480 ):  # 44480
            name = f'Thymio-{p}'
            r = Client.RobotControl.connect( name, host, port )
            robots.append( r)

        while( True ):
            for r in robots:
                r.setSpeed( random.uniform( -1000,1000 ), random.uniform( -1000,1000 ) )
            time.sleep( 2 )
    except ConnectionResetError:
        print( 'Conexion abortada' )
    except Exception as e:
        print( e )

    # Server shutdown
    pg.send_signal( subprocess.signal.SIGTERM )


# show time
main()
