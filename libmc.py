import socket
from mctypes import PackVarInt, ParseVarInt, ParseString, ParseLong, PackCoords, ParseCoords, PackString, PackUnsignedShort
from enum import Enum
import zlib

def hex_print(packet):
    print([hex(x) if isinstance(x, int) else hex(ord(x)) for x in packet])

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
    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port
        self.compression = False
        self.state = Login
        self.position = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        print("MCBot initialized")

    def recv(self, count):
        return self.sock.recv(count)

    def send(self, packet):
        if self.compression:
            packet = PackVarInt(0) + packet

        hex_print(packet)
        packet = [len(packet)] + packet
        packet = [ord(x) if isinstance(x, str) else x for x in packet]
        hex_print(packet)
        self.sock.send(bytes(packet))
    
    def get_packet_length(self, data):
        length = ParseVarInt(data)
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
        position, packet = ParseLong(packet, consume=True)
        x, y, z = ParseCoords(position)
        self.position = [x, y, z]
        return packet

    def send_PlayerPosition(self, x, y, z):
        print("Sending PlayerPosition (%s, %s, %s)" % (x, y, z))
        packet = PackVarInt(0x10) + PackCoords(x, y, z)
        self.send(packet)

    def handle_KeepAlive(self, packet):
        """TODO"""
        print("Play.KeepAlive")
        self.send_KeepAlive(packet)
        return []

    def send_KeepAlive(self, packet):
        print("Sending KeepAlive")
        packet = PackVarInt(0x0e) + packet
        self.send(packet)

    def handle_Disconnect(self, packet):
        """TODO"""
        print("Play.Disconnect")
        import sys; sys.exit(-1)
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
        self.respawn()
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

    def send_HandShake(self):
        """Server Handshake"""
        print("Sending Server HandShake")
        packet = PackVarInt(0) + PackVarInt(404) + PackString(self.host) + PackUnsignedShort(self.port) + PackVarInt(2)
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

    def respawn(self):
        self.send_ClientStatus(0)

    def run(self):
        print("MCBot running...")
        self.send_HandShake()
        self.send_LoginStart()

        packet = []
        while True:
            data = self.recv(1)
            if data:
                data = data[0]
                packet.append(data)

                # If we see that we got VarInt, start parsing
                if data & 0b10000000 == 0:
                    length = self.get_packet_length(packet)

                    # Hack to make sure socket gets all bytes
                    packet = []
                    while len(packet) < length:
                        packet.append(self.recv(1)[0])
                    assert len(packet) == length, "Length is somehow different! (%s != %s)" % (len(packet), length)
                    print("%s bytes: " % length, end="")

                    # Now that we have the packet handle it
                    try:
                        self.handle_packet(packet)
                    except:
                        print([hex(x) for x in packet])
                        self.handle_packet(packet)
                    packet = []
