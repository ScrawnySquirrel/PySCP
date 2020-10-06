import sys
import socket
import os

serverIP = 'localhost'
clientIP = 'localhost'

controlHost = ''
controlPort = 7005

dataHost = ''
dataPort = 7006

dirName = 'fileshare'
dirPath = './'+dirName

pcktSize = 1024

def socket_bind_listen(host, port):
    sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sckt.bind((host, port))
    sckt.listen(5)
    return sckt

def send_data(sckt, data):
    sckt.sendall(data)
    return

def get_data(sckt):
    while True:
        data = sckt.recv(pcktSize)
        if not data:
            break
        print(data.decode('utf-8'))
    return

def send_file(sckt, filename):
    file = dirPath+"/"+filename

    with open(file, "rb") as f:
        data = f.read(pcktSize)
        while data:
            sckt.send(data)
            data = f.read(pcktSize)
    return

def get_file(sckt, filename):
    file = dirPath+"/"+filename
    with open(file, "wb") as f:
        while True:
            data = sckt.recv(pcktSize)
            if not data:
                break
            f.write(data)
    return

def send_request(sckt, req):
    sckt.sendall(req.encode('utf-8'))
    return

def get_request(client_connection, client_address):
    while True:
        data = client_connection.recv(pcktSize)
        print(client_address+": "+data.decode('utf-8'))
        if not data:
            break
        else:
            server_request_handler(data.decode('utf-8'), client_address)
    return

def client_request_handler(ctrl_sckt, req_arr):
    if req_arr[0] == 'list':
        send_request(ctrl_sckt, stringify_list(req_arr))
        ds = socket_bind_listen(dataHost, dataPort)
        dsConnection, dsAddress = ds.accept()
        get_data(dsConnection)
    elif req_arr[0] == 'get':
        if len(req_arr) < 2:
            print("Not enough parameters")
            return
        send_request(ctrl_sckt, stringify_list(req_arr))
        ds = socket_bind_listen(dataHost, dataPort)
        dsConnection, dsAddress = ds.accept()
        get_file(dsConnection, req_arr[1])
        ds.close()
    elif req_arr[0] == 'send':
        if len(req_arr) < 2:
            print("Not enough parameters")
            return
        send_request(ctrl_sckt, stringify_list(req_arr))
        ds = socket_bind_listen(dataHost, dataPort)
        dsConnection, dsAddress = ds.accept()
        send_file(dsConnection, req_arr[1])
        ds.close()
    elif req_arr[0] == 'quit':
        print("Bye")
        sys.exit()
    else:
        print("Unknown command")
    return

def server_request_handler(req, client_address):
    clientIP=client_address
    req_arr = tokenize_string(req)
    if req_arr[0] == 'list':
        ds = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ds.connect((clientIP,dataPort))
        send_data(ds, server_list_files().encode('utf-8'))
        ds.close()
    elif req_arr[0] == 'get':
        ds = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ds.connect((clientIP,dataPort))
        send_file(ds, req_arr[1])
        ds.close()
    elif req_arr[0] == 'send':
        ds = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ds.connect((clientIP,dataPort))
        get_file(ds, req_arr[1])
        ds.close()
    else:
        ds = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ds.connect((clientIP,dataPort))
        send_data(ds, "Unknown command".encode('utf-8'))
        ds.close()
    return

def get_user_input():
    input_str = input("Command: ")
    input_arr = tokenize_string(input_str)
    return input_arr

def tokenize_string(str):
    arr = str.split()
    arr[0] = arr[0].lower()
    return arr

def stringify_list(arr):
    str = " "
    return str.join(arr)

def create_fileshare():
    if not os.path.exists(dirPath):
        os.mkdir(dirName)
    return

def server_list_files():
    files = os.listdir(dirPath)
    if len(files) <= 0:
        return "No file(s) found"
    return stringify_list(files)
