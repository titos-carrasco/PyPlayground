from pyplayground.server.Playground import Playground

# THE main
def main():
    # Levantamos el playground en este proceso y quedamos a la espera de conexiones
    Playground( "worlds/simple.world" ).run()

# show time
main()
