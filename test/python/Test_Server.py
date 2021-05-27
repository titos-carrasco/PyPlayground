from pyplayground.server.Playground import Playground

class TestServer():
    def __init__( self ):
        pass

    def run( self):
        # Levantamos el playground en este proceso y quedamos a la espera de conexiones
        Playground( "../worlds/simple.world" ).run()

# show time
TestServer().run()
