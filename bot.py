"""Minecraft bot"""
import socket
import struct
from mctypes import *
import libmc

def main():
    """do the thing"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 25565
    host = "127.0.0.1"
    sock.connect((host, port))

    # Handshake
    packet = PackVarInt(0) + PackVarInt(404) + PackString(host) + PackUnsignedShort(port) + PackVarInt(2)
    packet = bytes([len(packet)] + [ord(x) for x in packet])
    sock.send(packet)

    # Login start
    packet = PackVarInt(0) + PackString("top1_2_new")
    packet = bytes([len(packet)] + [ord(x) for x in packet])
    sock.send(packet)

    # Main loop
    packet = []

    mc = libmc.libmc()
    while True:
        data = sock.recv(1)
        if data:
            data = data[0]
            packet.append(data)
            if data & ~0b10000000:
                length = mc.get_packet_length(packet)
                print(len(packet))
                print(length)
                packet = sock.recv(length)
                mc.handle_packet(packet)
                packet = []

if __name__ == "__main__":
    main()