"""Minecraft bot"""
import socket
import struct
from mctypes import *

def main():
    """do the thing"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 25565
    host = "127.0.0.1"
    sock.connect((host, port))

    packet = PackVarInt(0) + PackVarInt(404) + PackString(host) + PackUnsignedShort(port) + PackVarInt(2)
    packet = bytes([len(packet)] + [ord(x) for x in packet])
    sock.send(packet)

    packet = PackVarInt(0) + PackString("top1_2_new")
    packet = bytes([len(packet)] + [ord(x) for x in packet])
    sock.send(packet)

    while True:
        data = sock.recv(1)
        if data & 0b10000000:
            packet = [data]

                


if __name__ == "__main__":
    main()