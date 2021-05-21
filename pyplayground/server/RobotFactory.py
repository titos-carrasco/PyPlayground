import server.RobotThymio2 as RobotThymio2
import server.RobotEPuck as RobotEPuck

# Factory
def makeRobot( tipo, name ):
    if( tipo == 'thymio2' ):
        return RobotThymio2.MyThymio2( name )
    elif( tipo == 'epuck' ):
        return RobotEPuck.MyEPuck( name )
    else:
        return None
