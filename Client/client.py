import socket
import os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to_server(server, port):
    client.connect((server, port))

def menu():
    print("\n========================================================")
    print("\n        Halo, Selamat Datang di Layanan FTP Kami!")
    print("\n========================================================")
    print("\n        Silakan Pilih Layanan: ")
    print("\n        1. CONN")
    print("\n        2. Upload <filename>")
    print("\n        3. Download <filename>")
    print("\n        4. List (list)")
    print("\n        5. JML")
    print("\n        6. rank")
    print("\n        7. Quit (quit)")
    print("\n========================================================")

path = os.getcwd()
menu()

status = True
connectionFlag = False
while status:
    cmd_input = input("Insert a command: ")
    if cmd_input.split(" ")[0] == "CONN" and connectionFlag == False:
        try:
            connect_to_server("127.0.0.1", 8085) #26.54.185.10 server radmin 
            connectionFlag = True
            print("Connection sucessful \n")
        except:
            print("Connection unsucessful. Make sure the server is online. \n")
    elif cmd_input == "JML":
        client.sendall(bytes(cmd_input, "UTF-8"))
    elif cmd_input == "rank":
        client.sendall(bytes(cmd_input, "UTF-8"))
    elif cmd_input == "list":
        client.sendall(bytes("List", "UTF-8"))
        buff = client.recv(1024)
        msg = buff.decode()
        print("List of files in directory:\n" + msg)
    elif cmd_input.split(" ")[0] == "Download":
        client.sendall(bytes(cmd_input, "UTF-8"))
        buff = client.recv(1024)
        if buff.decode() == "No file found":
            os.system("cls")
            menu()
            print("Invalid file\n")
        else:
            print("Received File From Server\n")
            f = open(cmd_input.split(" ")[1], "wb")
            f.write(buff)
            f.close()
            msg = buff.decode()
            jml_down = jml_down + 1
    elif cmd_input.split(" ")[0] == "Upload":
        fileName = cmd_input.split(" ")[1]
        if os.path.isfile(fileName):
            client.sendall(bytes(cmd_input, "UTF-8"))
            f = open(fileName, "rb")
            contents = f.read(1024)
            client.send(contents)
            print("File Stored on Server\n")
            jml_up = jml_up + 1
            client.send(bytes("end", "UTF-8"))
            f.close()
        else:
            print("Invalid file\n")
    elif cmd_input == "quit":
        client.sendall(bytes("quit", "UTF-8"))
        client.close()
        status = False
    else:
        print("Invalid command \n")
        menu()
