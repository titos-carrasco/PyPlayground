import time
import random
import subprocess

from pyplayground.client import Client


def setDicc( val ):
    dicc = {}
    for i in range(3,23):
        dicc[ i ] = val
    return dicc

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
        thymio = Client.RobotControl.connect( 'Thymio-01', host, port )
        epuck  = Client.RobotControl.connect( 'Epuck-01' , host, port )
        epuck.setLedRing( True )

        led = False
        t = 0
        while( True ):
            if( time.time() - t > 1 ):
                thymio.setLedsIntensity( setDicc( led ) )
                led = not led
                t = time.time()

            time.sleep( 0.001 )


    except ConnectionResetError:
        print( 'Conexion abortada' )
    except Exception as e:
        print( e )

    # Server shutdown
    pg.send_signal( subprocess.signal.SIGTERM )


# show time
main()
