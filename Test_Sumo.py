import time
import random
import subprocess

from pyplayground.client import RobotFactory

# THE main
def main():
    # Levantamos el playground en otro proceso
    try:
        pg = subprocess.Popen( [ 'python', 'pyplayground/server/Playground.py', 'worlds/sumo.world' ], shell=False )
        time.sleep( 1 )
    except Exception as e:
        print( e )
        exit()

    # Los datos de conexion al playground
    host = '127.0.0.1'
    port = 44444

    # Usamos try/except para conocer los errores que se produzcan
    speed = 100
    try:
        # Accesamos el robot y configuramos algunos de sus atributos
        rob = RobotFactory.connectRobot( 'Thymio-01', host, port )
        rob.setSpeed( speed, speed )

        # Loop clasico
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

    # Detenemos el playground
    pg.send_signal( subprocess.signal.SIGTERM )

# show time
main()
