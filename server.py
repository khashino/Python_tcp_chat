import select
import socket
import sys
import traceback


def send_to_all(sock,msg):
    for socket in connected_list:
        if socket != server_socket and socket != sock:
            try:
                socket.send(msg)
            except:
                socket.close()
                connected_list.remove(socket)


if __name__ == "__main__":

    name = ""
    record = {}
    connected_list = []

    buffer = 4096
    port = 8888

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", port))
    server_socket.listen(10)

    connected_list.append(server_socket)

    print("\033[32mServer Started\033[0m")



    while 1:
        rList, wList, error_socket = select.select(connected_list, [], [])

        for sock in rList:
            # new Connection
            if sock == server_socket:
                sockfd, addr = sock.accept()
                name = sockfd.recv(buffer)
                connected_list.append(sockfd)
                record[addr] = ""

                if name in record.values():
                    sockfd.send('name exist!!!')
                    del record[addr]
                    connected_list.remove(sockfd)
                    sockfd.close()
                    continue
                else:
                    record[addr] = name
                    print ("client (%s, %s) connected" % addr, " [", record[addr], "]")
                    sockfd.send("\33[32m\r\33[1m Welcome to Server for exit type byebye\n\33[0m")
                    #### send to all that im here
                    send_to_all(sock, "\33[32m\r\33[1m\r"+name+" joined conversation\n\33[0m")

            #New Msg
            else:
                try:
                    data1 = sock.recv(buffer)
                    try:
                        data=data1[:data1.index("\n")]
                    except:
                        data = data1
                    i, p = sock.getpeername()
                    print("\33[31m\33[1mLOG\t\33[0m" + record[(i, p)] + ":" + data)
                    if data == "byebye":
                        send_to_all(sock,record[(i, p)]+" left server")
                        print (record[(i, p)]+" left server")
                        del record[(i, p)]
                        connected_list.remove(sock)
                        sock.close()
                        continue

                    else:
                        msg="\r\33[31m\33[1m"+record[(i, p)]+":\33[0m "+data+"\n"
                        send_to_all(sock,msg)
                except Exception:
                    traceback.print_exc(file=sys.stdout)
                    (i, p)=sock.getpeername()
                    send_to_all(sock,"\33[32m\r\33[1m"+record[(i, p)]+" left server\n\33[0m")
                    print (record[(i, p)]+" left server")
                    del record[(i, p)]
                    connected_list.remove(sock)
                    sock.close()
                    continue

    server_socket.close()