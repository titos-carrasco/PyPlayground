import socket
import json


#--- Envia un diccionaro en formato JSON
def send( sock, dicc ):
    msg = json.dumps( dicc ) + '\n'
    try:
        sock.sendall( bytearray( msg, 'utf-8' ) )
    except Exception as e:
        raise

#--- Recibe un string en formato JSON y retorna un diccionario
def read( sock, buff ):
    lbuff = len( buff )
    n = 0
    while( n < lbuff ):
        c = sock.recv( 1 )
        if( not c ): raise ConnectionResetError
        if( c == b'\n' ): break;
        buff[n] = c[0]
        n += 1
    return json.loads( buff[:n].decode( 'utf-8' ) )

