import time
import random
import subprocess

from pyplayground.client import Client


#---
def main():
    # Server
    try:
        pg = subprocess.Popen( [ 'python', 'pyplayground/server/Playground.py', 'worlds/sumo.world' ], shell=False )
        time.sleep( 1 )
    except Exception as e:
        print( e )
        exit()

    # Client
    host = '127.0.0.1'
    port = 44444
    speed = 100
    try:
        rob = Client.RobotControl.connect( 'Thymio-01', host, port )
        rob.setSpeed( speed, speed )
        while( True ):
            sensores = rob.getSensors()

            print( 'proximitySensorValues:' , end='' )
            s = sensores['proximitySensorValues']
            for v in s:
                print( '%-5.2f ' % v , end='' )
            print()

            print( 'proximitySensorDistances:' , end='' )
            s = sensores['proximitySensorDistances']
            for v in s:
                print( '%-5.2f ' % v , end='' )
            print()

            print( 'groundSensorValues:' , end='' )
            s = sensores['groundSensorValues']
            for v in s:
                print( '%-5.2f ' % v , end='' )
            print( '\n' )

            gl = sensores['groundSensorValues'][0]
            gr = sensores['groundSensorValues'][1]
            if( gl < 200 or gr < 200 ):
                rob.setSpeed( -speed, -speed )
                time.sleep( 2 )
                rob.setSpeed( -speed, speed )
                time.sleep( 2 )
                rob.setSpeed( speed, speed )
            time.sleep( 0.001 )
    except ConnectionResetError:
        print( 'Conexion abortada' )
    except Exception as e:
        print( e )

    # Server shutdown
    pg.send_signal( subprocess.signal.SIGTERM )


# show time
main()
