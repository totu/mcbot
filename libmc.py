from mctypes import ParseVarInt, ParseString, ParseLong
from enum import Enum
import zlib

class Login(Enum):
    Disconnect = 0x00
    EncryptionRequest = 0x01
    LoginSuccess = 0x02
    SetCompression = 0x03

class Play(Enum):
    Disconnect = 0x1b
    KeepAlive = 0x21 
    PluginMessage = 0x19
    JoinGame = 0x25
    ServerDifficulty = 0x0d
    PlayerAbilities = 0x2e
    HeldItemChange = 0x3d
    DeclareRecipes = 0x54
    Tags = 0x55
    CloseWindow = 0x13
    ChunkData = 0x22
    EntityStatus = 0x1c
    DeclareCommands = 0x11
    UnlockRecipes = 0x34
    PlayerInfo = 0x30
    SpawnPlayer = 0x05
    EntityMetadata = 0x3f
    EntityProperties = 0x52
    PlayerPositionAndLook = 0x32
    WorldBorder = 0x3b
    TimeUpdate = 0x4a
    SpawnPosition = 0x49
    EntityRelativeMove = 0x28
    WindowItems = 0x15
    SetSlot = 0x17
    Advancements = 0x51
    UpdateHealth = 0x44
    BlockChange = 0x0b
    SetExperience = 0x43

class libmc():
    def __init__(self, sock):
        self.sock = sock
        self.compression = False
        self.state = Login
        self.position = []

    def recv(self, count):
        return self.sock.recv(count)

    def send(self, packet):
        self.sock.send(packet)
    
    def get_packet_length(self, data):
        try:
            length = ParseVarInt(data)
        except IndexError:
            print("FAIL!")
            print(data, bin(data[0]))
            import sys; sys.exit(-1)
        return length

    def handle_SetCompression(self, packet):
        """Threshold (VarInt): Maximum size of a packet before it is compressed"""
        threshold, packet = ParseVarInt(packet, consume=True)
        del threshold
        print("Login.SetCompression")
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

    def handle_DeclareRecipes(self, packet):
        """TODO"""
        print("Play.DeclareRecipes")
        return []

    def handle_Tags(self, packet):
        """TODO"""
        print("Play.Tags")
        return []

    def handle_CloseWindow(self, packet):
        """TODO"""
        # This is the ID of the window that was closed. 0 for inventory. 
        print("Play.CloseWindow")
        return []

    def handle_ChunkData(self, packet):
        """TODO"""
        # This is the ID of the window that was closed. 0 for inventory. 
        print("Play.ChunkData")
        return []

    def handle_EntityStatus(self, packet):
        """TODO"""
        print("Play.EntityStatus")
        return []

    def handle_DeclareCommands(self, packet):
        """TODO"""
        print("Play.DeclareCommands")
        return []

    def handle_UnlockRecipes(self, packet):
        """TODO"""
        print("Play.UnlockRecipes")
        return []

    def handle_PlayerInfo(self, packet):
        """TODO"""
        print("Play.PlayerInfo")
        return []

    def handle_SpawnPlayer(self, packet):
        """TODO"""
        print("Play.SpawnPlayer")
        return []

    def handle_EntityMetadata(self, packet):
        """TODO"""
        print("Play.EntityMetadata")
        return []

    def handle_EntityProperties(self, packet):
        """TODO"""
        print("Play.EntityProperties")
        return []

    def handle_PlayerPositionAndLook(self, packet):
        """TODO"""
        print("Play.PlayerPositionAndLook")
        return []

    def handle_WorldBorder(self, packet):
        """TODO"""
        print("Play.WorldBorder")
        return []

    def handle_TimeUpdate(self, packet):
        """TODO"""
        print("Play.TimeUpdate")
        return []

    def handle_SpawnPosition(self, packet):
        print("Play.SpawnPosition")
        print(packet)
        position, packet = ParseLong(packet, consume=True)
        print(bin(position))
        return packet

    def handle_KeepAlive(self, packet):
        """TODO"""
        print("Play.KeepAlive")
        self.send_KeepAlive(packet)
        return []

    def send_KeepAlive(self, packet):
        self.send(bytes(packet))

    def handle_Disconnect(self, packet):
        """TODO"""
        print("Play.Disconnect")
        return []

    def handle_EntityRelativeMove(self, packet):
        """TODO"""
        print("Play.EntityRelativeMove")
        return []

    def handle_WindowItems(self, packet):
        """TODO"""
        print("Play.WindowItems")
        return []

    def handle_Advancements(self, packet):
        """TODO"""
        print("Play.Advancements")
        return []

    def handle_SetSlot(self, packet):
        """TODO"""
        print("Play.SetSlot")
        return []

    def handle_UpdateHealth(self, packet):
        """TODO"""
        print("Play.UpdateHealth")
        return []

    def handle_BlockChange(self, packet):
        """TODO"""
        print("Play.BlockChange")
        return []

    def handle_SetExperience(self, packet):
        """TODO"""
        print("Play.SetExperience")
        return []

        


    def handle_packet(self, packet):
        """Parse packet id and call appropriate handler"""
        if self.compression:
            compression_len, packet = ParseVarInt(packet, consume=True)

            # if we have compressed data decompress it
            if compression_len != 0:
                packet = zlib.decompress(bytearray(packet))
            
        packet_id, packet = ParseVarInt(packet, consume=True)
        try:
            packet_id = str(self.state(packet_id))
        except ValueError:
            print("Unknown packet ID %s for state %s" % (hex(packet_id), self.state))

        try:
            func = getattr(self, "handle_" + packet_id.split(".")[1])
            packet = func(packet=packet)
            assert len(packet) == 0
        except AttributeError:
            print("Unknown packet: %s" % packet)
            pass

