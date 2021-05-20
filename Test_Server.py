from pyplayground.server import Playground

# THE main
def main():
    # Levantamos el playground en este proceso y quedamos a la espera de conexiones
    Playground.Playground( 'worlds/simple.world' ).run()

# show time
main()
