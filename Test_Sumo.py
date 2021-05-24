import time
import random
import subprocess

from pyplayground.client.RobotThymio2 import RobotThymio2

# THE main
def main():
    # Levantamos el playground en otro proceso
    try:
        pg = subprocess.Popen( [ "python", "pyplayground/server/Playground.py", "worlds/sumo.world" ], shell=False )
        time.sleep( 1 )
    except Exception as e:
        print( e )
        exit()

    # Los datos de conexion al playground
    host = "127.0.0.1"
    port = 44444

    # Usamos try/except para conocer los errores que se produzcan
    speed = 100
    try:
        # Accesamos el robot y configuramos algunos de sus atributos
        rob = RobotThymio2( "Thymio-01", host, port )
        rob.setSpeed( speed, speed )

        # Loop clasico
        t = time.time()
        while( time.time() - t < 15 ):
            rob.getSensors()

            print( "pos:", rob.pos )
            print( "speed:", rob.speed )
            print( "proximitySensorValues:", rob.proximitySensorValues )
            print( "proximitySensorDistances:" , rob.proximitySensorDistances )
            print( "groundSensorValues:" , rob.groundSensorValues )

            gl = rob.groundSensorValues[0]
            gr = rob.groundSensorValues[1]
            if( gl < 200 or gr < 200 ):
                rob.setSpeed( -speed, -speed )
                time.sleep( 2 )
                rob.setSpeed( -speed, speed )
                time.sleep( 2 )
                rob.setSpeed( speed, speed )
            time.sleep( 0.001 )
        rob.setSpeed( 0, 0 )
        rob.close()
    except ConnectionResetError:
        print( "Conexion abortada" )
    except Exception as e:
        print( e )

    # Detenemos el playground
    pg.send_signal( subprocess.signal.SIGTERM )

# show time
main()
