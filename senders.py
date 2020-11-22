"""libmc senders"""
from mctypes import (
    PackVarInt,
    PackString,
    PackUnsignedShort,
    PackDouble,
    PackBool,
    PackFloat,
)


class Sender:
    def __init__(self):
        """Dummy init for inheritors"""
        self.name = None
        self.port = None
        self.host = None
        self.compression = None
        self.sock = None

    def send(self, packet):
        if self.compression:
            packet = PackVarInt(0) + packet

        packet = [len(packet)] + packet
        packet = [ord(x) if isinstance(x, str) else x for x in packet]
        self.sock.send(bytes(packet))

    def send_KeepAlive(self, packet):
        # print("Sending KeepAlive")
        packet = PackVarInt(0x0E) + packet
        self.send(packet)

    def send_HandShake(self):
        """Server Handshake"""
        print("Sending Server HandShake")
        packet = (
            PackVarInt(0)
            + PackVarInt(404)
            + PackString(self.host)
            + PackUnsignedShort(self.port)
            + PackVarInt(2)
        )
        self.send(packet)

    def send_LoginStart(self):
        """Login start"""
        print("Sending Server LoginStart")
        packet = PackVarInt(0) + PackString(self.name)
        self.send(packet)

    def send_ClientStatus(self, action_id):
        """Client Status"""
        print("Sending Server ClientStatus")
        packet = PackVarInt(0x03) + PackVarInt(action_id)
        self.send(packet)

    def send_TeleportConfirm(self, teleport_id):
        """Teleport Confirm"""
        print("Sending Server TeleportConfirm")
        packet = PackVarInt(0x00) + PackVarInt(teleport_id)
        self.send(packet)
        self.accepted_teleport = teleport_id

    def send_PlayerPosition(self, x, y, z):
        self.position = [x, y, z]
        # y = y - 1.62
        packet = (
            PackVarInt(0x10)
            + PackDouble(x)
            + PackDouble(y)
            + PackDouble(z)
            + PackBool(True)
        )
        self.send(packet)

    def send_PlayerLook(self, yaw, pitch):
        """Look at something"""
        packet = PackVarInt(0x12) + PackFloat(yaw) + PackFloat(pitch) + PackBool(True)
        self.send(packet)

    def send_PlayerPositionAndLook(self, x, y, z, yaw, pitch, on_ground=True):
        self.position = [x, y, z]
        self.yaw = yaw
        self.pitch = pitch
        packet = (
            PackVarInt(0x11)
            + PackDouble(x)
            + PackDouble(y)
            + PackDouble(z)
            + PackFloat(yaw)
            + PackFloat(pitch)
            + PackBool(on_ground)
        )
        self.send(packet)
