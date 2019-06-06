'''
Created on Oct 24, 2017

@author: wuh2
'''
from socket import *
import threading
import sys

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

class Talk:
    def __init__(self, serverName, serverPort, clientPort):
        self.serverName=serverName
        self.serverPort=serverPort
        self.clientPort=clientPort
        self.terminate=False
        
    def startServer(self):
        serverSocket=socket(AF_INET,SOCK_STREAM)
        serverSocket.bind(('',self.serverPort))
        serverSocket.listen(1)
        print("server ready!")
        while not self.terminate:
            try:
                connectionSocket,addr=serverSocket.accept()
                msg=connectionSocket.recv(1024).decode()
                if msg.upper()=='QUIT':
                    self.terminate=True;
                print(addr[0]+"> "+msg)
                connectionSocket.close()
            except:
                break
    
    def sendMsg(self):
        print("client ready")
        while not self.terminate:
            try:
                msg=input()
                print(CURSOR_UP_ONE+ERASE_LINE+"me> "+msg)
                sys.stdout.flush()
                clientSocket=socket(AF_INET,SOCK_STREAM)
                clientSocket.connect((self.serverName,self.clientPort))
                clientSocket.send(msg.encode())
                clientSocket.close()
                if msg.upper()=='QUIT':
                    self.terminate=True;
            except:
                break
    
    def run(self):
        t1 = threading.Thread(target=self.startServer)
        t2 = threading.Thread(target=self.sendMsg)
        t1.start()
        t2.start()
        
def main(argv):
    serverIP=argv[1]
    serverPort=int(argv[2])
    clientPort=int(argv[3])
    print("start")
    t1=Talk(serverIP, serverPort, clientPort)
    t1.run()
    
main(sys.argv)
