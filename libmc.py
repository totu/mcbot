from mctypes import ParseVarInt, ParseString
from enum import Enum

class Login(Enum):
    Disconnect = 0x00
    EncryptionRequest = 0x01
    LoginSuccess = 0x02
    SetCompression = 0x03

class Play(Enum):
    PluginMessage = 0x19
    JoinGame = 0x25
    ServerDifficulty = 0x0d
    PlayerAbilities = 0x2e
    HeldItemChange = 0x3d

class libmc():
    def __init__(self):
        self.compression = False
        self.state = Login

    def get_packet_length(self, data):
        try:
            length = ParseVarInt(data)
        except IndexError:
            print("FAIL!")
            print(data, bin(data[0]))
            import sys; sys.exit(-1)
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
        del uuid, username
        print("Login.LoginSucess")
        self.state = Play
        return packet

    def handle_JoinGame(self, packet):
        """TODO"""
        print("Play.JoinGame")
        return []

    def handle_PluginMessage(self, packet):
        """TODO"""
        print("Play.PluginMessage")
        return []

    def handle_ServerDifficulty(self, packet):
        """TODO"""
        print("Play.ServerDifficulty")
        return []

    def handle_PlayerAbilities(self, packet):
        """TODO"""
        print("Play.PlayerAbilities")
        return []

    def handle_HeldItemChange(self, packet):
        """TODO"""
        print("Play.HeldItemChange")
        return []

    def handle_packet(self, packet):
        """Parse packet id and call appropriate handler"""
        if self.compression:
            compression_len, packet = ParseVarInt(packet, consume=True)
            assert compression_len == 0, "This needs to be handled now, fuckboi!"
            
        packet_id, packet = ParseVarInt(packet, consume=True)
        try:
            packet_id = str(self.state(packet_id))
        except ValueError:
            print("Unknown packet ID %s for state %s" % (hex(packet_id), self.state))

        func = getattr(self, "handle_" + packet_id.split(".")[1])
        packet = func(packet=packet)
        assert len(packet) == 0

