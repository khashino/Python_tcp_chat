import select
import socket
import sys

def display():
    you = "\n\33[34m\33[1mYou: \033[0m"
    sys.stdout.write(you)
    sys.stdout.flush()


def main():
    host = raw_input("\33[34m\33[1mEnter server ip address: \033[0m")
    #host = '127.0.0.1'
    port = 8888
    name = ""

    name = raw_input("\33[34m\33[1mEnter Your Username: \033[0m")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try:
        s.connect((host, port))
    except:
        print ("\33[31m\33[1mServer Not Found!!!\033[0m")
        sys.exit()


    s.send(name)
    display()

    while 1:
        socket_list = [sys.stdin, s]

        rList, wList, error_socket = select.select(socket_list, [], [])

        for sock in rList:
            #incoming msg
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    print ("DISCONNECTED!!!")
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    display()
            #user msg
            else:
                msg = sys.stdin.readline()
                s.send(msg)
                display()



if __name__ == "__main__":
    main()