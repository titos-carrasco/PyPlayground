import time
import random
import subprocess

from pyplayground.client import Client


#---
def main():
    # Server
    try:
        pg = subprocess.Popen( [ 'python', 'pyplayground/server/Playground.py', 'worlds/simple.world' ], shell=False )
        time.sleep( 1 )
    except Exception as e:
        print( e )
        exit()

    # Client
    host = '127.0.0.1'
    port = 44444
    try:
        rob01 = Client.RobotControl.connect( 'Thymio-01', host, port )
        rob02 = Client.RobotControl.connect( 'Epuck-01', host, port )

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

    # Server shutdown
    pg.send_signal( subprocess.signal.SIGTERM )


# show time
main()
