import socket
import threading
import os

def downloadFile(name,sock):
    filename = sock.recv(1024)
    if os.path.isfile(filename):
        sock.sendall("Exists" +str(os.path.getsize(filename,'utf-8')))
        userResponse = sock.recv(1024)
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytestoSend = f.read(1024)
                sock.sendall(bytestoSend)
                while bytestoSend != "":
                    bytestoSend = f.read(1024)
                    sock.sendall(bytestoSend)
    else:
        sock.sendall("ERR")

    sock.close()

def main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.bind((host,port))

    s.listen(5)

    print("Server started and ready to recieve")
    while True:
        c, addr = s.accept()
        print("client connected from ip:<" +str(addr) + ":")
        t = threading.Thread(target=downloadFile, args=("downThread",c))
        t.start()

    s.close()

if __name__== '__main__':
    main()
    
