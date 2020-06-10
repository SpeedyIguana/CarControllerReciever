import socket
import struct
import sys
import netifaces
import time
import json

possibleStates = [
    "listening", # 0
    "connected" # 1
]

def getIP(interface = "eth0"):
    return netifaces.ifaddresses(interface)[2][0]['addr']

possibleMsgsAndCorrespondingFunctions = {
    "quit": closeConnection,
    "headlight": toggleHeadlight
}

ServerIP = getIP()
ServerPort = 42069

def closeConnection(state, connection, sock):
    print("closing")
    connection.close()
    state = possibleStates[1]
    sock.close()

def toggleHeadlight(state, connection, sock):
    pass

def handleMessage(recvdMsg, frState, state, connection, sock):
    msg = recvdMsg.decode('ascii')
    if msg in possibleMsgsAndCorrespondingFunctions.keys():
        print(msg)
        possibleMsgsAndCorrespondingFunctions[msg](state, connection, sock)
        return frState
    else:
        try:
            decoded = json.loads(msg)
            forward = decoded['f']
            right = decoded['r']
            print("r =", right, "\tf =", forward)
            rtn = (right, forward)
            return rtn
        except:
            print("too much data")
            return frState

def startSocket():
    server_address = (ServerIP, ServerPort)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(server_address)
    return sock
