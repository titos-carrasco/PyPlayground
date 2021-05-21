import socket
import json


def send( sock:socket.socket, dicc:dict ) -> None :
    """
    Convierte el diccionario recibido a un string en formato
    JSON, agregando un '\\n' al final, y lo envia por el socket

    Parameters
      sock: El socket a utilizar
      dicc: El diccionario a enviar
    """
    msg = json.dumps( dicc ) + '\n'
    try:
        sock.sendall( bytearray( msg, 'utf-8' ) )
    except Exception as e:
        raise

def read( sock:socket.socket, buff:bytearray ) -> dict :
    """
    Lee del socket un string en formato JSON, finalizado en '\\n',
    y lo convierte a un diccionario

    Parameters
      sock:  El socket a utilizar.
      buff:  Buffer temporal de lectura.
             Se leeran hasta "len(bytearray)" bytes

    Return
      El diccionario
    """

    lbuff = len( buff )
    n = 0
    while( n < lbuff ):
        c = sock.recv( 1 )
        if( not c ): raise ConnectionResetError
        if( c == b'\n' ): break;
        buff[n] = c[0]
        n += 1
    return json.loads( buff[:n].decode( 'utf-8' ) )

