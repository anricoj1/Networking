import socket

def main():
    host= '127.0.0.1'
    port= 5000

    s = socket.socket()
    s.connect((host,port))

    filename = input("filename:> ")
    if filename != 'q':
        s.sendall(filename.encode('utf-8'))
        data = s.recv(1024)
        if data[:6] == 'Exists':
            filesize = long(data[6:])
            message = input("File Exists, "+str(filesize)+\
                                "Bytes, download? (Y/N)? : ")
            if message == 'Y':
                s.sendall('OK')
                f = open('new_'+filename, 'wb')
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print("{0:.2f}".format((totalRecv/float(filesize))*100)+\
                          "% Done")
                    print("Download complete")
        else:
            print("File does not Exist!")
    s.close()


if __name__== '__main__':
    main()

