import re
import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


"""
The below function gets the latest messages from the server and inserts it into the Listbox object.
If the window has somehow been closed abruptly, we remove the user.
"""
def receive():
    stop = False
    clientSocket.send(bytes(myUser.get(), 'utf-8'))
    while True and not stop:
        try:
            msg = clientSocket.recv(BUFFSIZE)
            #print (str(msg))
            reaesc = re.compile(r'\x1b[^m]*m')
            new_text = reaesc.sub('', msg.decode("utf-8"))
            #print (new_text)
            msgList.insert(tkinter.END, new_text)
        except OSError:
            cleanAndClose()
            break



"""
The below function sends the messages of the user to the server to be broadcast, 
if the exit sequence is entered, user's data is purged, and the window is closed.
"""
def send(event=None):
    while True:
        try:
            msg = myMsg.get()
            myMsg.set("")
            clientSocket.send(bytes(msg, 'utf-8'))
            msgList.insert(tkinter.END, "You: "+msg)
            break
        except OSError:
            cleanAndClose()
            break

"""
If the exit sequence is entered, this function is executed.
"""
def cleanAndClose(event=None):
    myMsg.set("byebye")
    send("byebye")
    top2.destroy()
    stop = True

def connect(event=None):
    top.destroy()

    global top2

    top2 = tkinter.Tk()
    top2.title('ChatRoom')

    global clientSocket
    global msgList
    global myMsg
    global BUFFSIZE
    #global clientSocket

    messageFrame = tkinter.Frame(top2)
    scrollbar = tkinter.Scrollbar(messageFrame)

    msgList = tkinter.Listbox(messageFrame, width = 50, yscrollcommand = scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msgList.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msgList.pack(fill = tkinter.X)
    messageFrame.pack()

    myMsg = tkinter.StringVar()
    myMsg.set("Click to type")
    entryField = tkinter.Entry(top2,textvariable = myMsg)
    entryField.bind("<Return>", send)
    entryField.pack()
    sendButton = tkinter.Button(top2, text = 'Send', command = send, height = 1, width = 7)
    sendButton.pack()

    top2.protocol("WM_DELETE_WINDOW", cleanAndClose)

    HOST = myServer.get()
    PORT = 8888
    #PORT = 5545 if not PORT else int(PORT)


    BUFFSIZE = 4096
    ADDR = (HOST, PORT)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    try:
        clientSocket.connect(ADDR)
    except:
        top2.destroy
        exit()


    receiveThread = Thread(target=receive)
    receiveThread.start()

    top2.mainloop()

    receiveThread.join()


if __name__ == '__main__':
    top = tkinter.Tk()
    top.title('ChatRoom')

    global username


    messageFrame = tkinter.Frame(top)
    scrollbar = tkinter.Scrollbar(messageFrame)

    myServer = tkinter.StringVar()
    myServer.set("127.0.0.1")
    entryField = tkinter.Entry(top, textvariable=myServer)
    entryField.pack()

    myUser = tkinter.StringVar()
    myUser.set("Your Name")
    entryField = tkinter.Entry(top, textvariable=myUser)
    entryField.pack()


    connectBtn = tkinter.Button(top, text='Connect', command=connect, height=1, width=10)
    connectBtn.pack()

    top.mainloop()