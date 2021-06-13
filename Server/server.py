import socket
import os
from _thread import *

LOCALHOST = "127.0.0.1" #"26.54.185.10" #ip server radmin
PORT = 8085
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((LOCALHOST, PORT))
server.listen(10)

print("Server started")
print("Waiting for client request...")
msg = ""
path = os.getcwd()

ThreadCount = 0
arr_jml = []

def rankUp(array):
	return sorted(array, reverse=True, key = lambda  x: x['jml_up'])

def rankDwn(array):
	return sorted(array, reverse=True, key = lambda  x: x['jml_dwn'])

def threaded_client(clientConnection,clientAddress,jml):
    status = True
    jml["ip"] = clientAddress[0]
    while status:
        in_data = clientConnection.recv(1024)
        msg = in_data.decode()
        if msg == "quit":
            print("Client ", clientAddress[0] ," disconnected...\n")
            status = False
        
        elif msg.split(" ")[0] == "List":
            files = os.listdir(path)
            file_string = ""
            for f in files:
                file_string += f
                file_string += ", "
            clientConnection.send(bytes(file_string, "UTF-8"))
            print("List Sent to ", clientAddress[0])

        elif msg.split(" ")[0] == "JML":
            print("Client IP : ",jml["ip"])
            print("jumlah upload : ",jml["jml_up"])
            print("jumlah download : ",jml["jml_dwn"])
        
        elif msg.split(" ")[0] == "rank":
            #upload
            topU = rankUp(arr_jml)[0]["ip"]
            up = rankUp(arr_jml)[0]["jml_up"]
            print("Client Dengan Upload Terbanyak: ",topU)
            print("Dengan Upload : ",up)
            #download
            topD = rankDwn(arr_jml)[0]["ip"]
            dwn = rankDwn(arr_jml)[0]["jml_dwn"]
            print("Client Dengan Download Terbanyak: ",topD)
            print("Dengan Download : ",dwn)

        elif msg.split(" ")[0] == "Download":
            fileName = msg.split(" ")[1]
            print('Download file... ', fileName)
            if os.path.isfile(fileName):
                with open(fileName, "rb") as f:
                    contents = f.read(1024)
                    while contents:
                        clientConnection.send(contents)
                        contents = f.read(1024)
                    print("File Sent to User\n")
                    clientConnection.send(bytes("end", "UTF-8"))
                f.close()
                jml["jml_dwn"] += 1
            else:
                clientConnection.send(bytes("No file found", "UTF-8"))
        elif msg.split(" ")[0] == "Upload":
            f = open(msg.split(" ")[1], "wb")
            print('Upload file... ', f)
            buff = clientConnection.recv(1024)
            print("File Upload on Server\n")
            f.write(buff)
            f.close()
            msg = buff.decode()
            jml["jml_up"] += 1
        else:
            print("Not a valid command, please input another command\n")
            clientConnection.send(bytes("Not a Valid command", "UTF-8"))
            break
    
while True:
    jml = {
        "ip": "",
        "jml_up": 0,
        "jml_dwn": 0
    }
    clientConnection, clientAddress = server.accept()
    print("Connected client :", clientAddress)
    start_new_thread(threaded_client, (clientConnection,clientAddress,jml))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
    arr_jml.append(jml)

print("Client disconnected...\n")
clientConnection.close()
