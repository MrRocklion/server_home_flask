import socket
def enviarDato(angulo):
    s = socket.socket()
    print(angulo)
    if(angulo <255):
        s.connect(('192.168.1.5',8090)) 
        s.send(angulo.to_bytes(1, 'big'))
        s.close()
        print("me desconecto")
    else:
        print("angulo muy alto")

enviarDato(10)