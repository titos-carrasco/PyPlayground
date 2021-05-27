import pyplayground

import pyplayground.server
import pyplayground.server.Playground
import pyplayground.server.RobotBase
import pyplayground.server.RobotEPuck
import pyplayground.server.RobotThymio2

import pyplayground.client
import pyplayground.client.RobotBase
import pyplayground.client.RobotEPuck
import pyplayground.client.RobotThymio2


class TestHelp():
    def __init__( self ):
        pass

    def run( self ):
        # Utilice la tecla "q" para avanzar entre cada pantalla de ayuda
        help( pyplayground )
        help( pyplayground.server )
        help( pyplayground.server.Playground )
        help( pyplayground.server.RobotBase )
        help( pyplayground.server.RobotEPuck )
        help( pyplayground.server.RobotThymio2 )
        help( pyplayground.client )
        help( pyplayground.client.RobotBase )
        help( pyplayground.client.RobotEPuck )
        help( pyplayground.client.RobotThymio2 )


# show time
TestHelp().run()
