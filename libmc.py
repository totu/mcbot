from mctypes import ParseVarInt, ParseString
from enum import Enum

class Login(Enum):
    Disconnect = 0x00
    EncryptionRequest = 0x01
    LoginSuccess = 0x02
    SetCompression = 0x03

class libmc():
    def __init__(self):
        self.compression = False

    def get_packet_length(self, data):
        length = ParseVarInt(data)
        return length

    def handle_Disconnect(self, packet):
        """Reason (Chat):"""
        l = len([x for x in packet])
        print(l, packet)
        return []

    def handle_SetCompression(self, packet):
        """Threshold (VarInt): Maximum size of a packet before it is compressed"""
        threshold, packet = ParseVarInt(packet, consume=True)
        print("Max packet size before compression: %s" % threshold)
        self.compression = True
        return packet

    def handle_LoginSuccess(self, packet):
        """UUID (string(36)): Unlike in other packets, this field contains the UUID as a string with hyphens.
           Username (string(16)):
        """
        uuid, packet = ParseString(packet, 36, consume=True)
        username, packet = ParseString(packet, 16, consume=True)
        print(uuid, username)
        return packet

    def handle_packet(self, packet):
        """Parse packet id and call appropriate handler"""
        if self.compression:
            compression_len, packet = ParseVarInt(packet, consume=True)        
            assert compression_len == 0, "This needs to be handled now, fuckboi!"
            
        packet_id, packet = ParseVarInt(packet, consume=True)
        packet_id = str(Login(packet_id))
        print(packet_id)

        #func = locals()["handle_" + packet_id.split(".")[1]]
        func = getattr(self, "handle_" + packet_id.split(".")[1])
        packet = func(packet=packet)
        assert len(packet) == 0

