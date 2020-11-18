import _thread
import time
import socket
from mctypes import *
from enum import Enum
import zlib
import math
import copy

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
    EntityTeleport = 0x50
    EntityLookAndRelativeMove = 0x29

class libmc():
    def __init__(self, name, host, port):
        self.names = {}
        self.entities = {}
        self.reading = False
        self.name = name
        self.host = host
        self.port = port
        self.compression = False
        self.state = Login
        self.position = []
        self.accepted_teleport = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.lock = _thread.RLock()
        print("MCBot initialized")

    def recv(self, count):
        return self.sock.recv(count)

    def send(self, packet):
        if self.compression:
            packet = PackVarInt(0) + packet

        packet = [len(packet)] + packet
        packet = [ord(x) if isinstance(x, str) else x for x in packet]
        self.sock.send(bytes(packet))
    
    def get_packet_length(self, data):
        length = ParseVarInt(data)
        return length

    def calculate_yaw_and_pitch(self, x, y, z):
        try:
            x0, y0, z0 = self.position
            dx = x-x0
            dy = y-y0
            dz = z-z0
            r = math.sqrt(dx*dx + dy*dy + dz*dz)
            yaw = -math.atan2(dx,dz)/math.pi*180
            if yaw < 0:
                yaw = 360 + yaw
            pitch = -math.asin(dy/r)/math.pi*180
        except ZeroDivisionError:
            return self.yaw, self. pitch

        self.yaw = yaw
        self.pitch = pitch
        return yaw, pitch

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
        # print("Play.PluginMessage")
        return []

    def handle_ServerDifficulty(self, packet):
        """TODO"""
        # print("Play.ServerDifficulty")
        return []

    def handle_PlayerAbilities(self, packet):
        """TODO"""
        # print("Play.PlayerAbilities")
        return []

    def handle_HeldItemChange(self, packet):
        """TODO"""
        # print("Play.HeldItemChange")
        return []

    def handle_DeclareRecipes(self, packet):
        """TODO"""
        # print("Play.DeclareRecipes")
        return []

    def handle_Tags(self, packet):
        """TODO"""
        # print("Play.Tags")
        return []

    def handle_CloseWindow(self, packet):
        """TODO"""
        # This is the ID of the window that was closed. 0 for inventory. 
        # print("Play.CloseWindow")
        return []

    def handle_ChunkData(self, packet):
        """TODO"""
        # This is the ID of the window that was closed. 0 for inventory. 
        # print("Play.ChunkData")
        return []

    def handle_EntityStatus(self, packet):
        """TODO"""
        # print("Play.EntityStatus")
        return []

    def handle_DeclareCommands(self, packet):
        """TODO"""
        # print("Play.DeclareCommands")
        return []

    def handle_UnlockRecipes(self, packet):
        """TODO"""
        # print("Play.UnlockRecipes")
        return []
        
    def _player_action_zero(self, count, packet):
        for i in range(int(len(packet)/count)):
            pckt = packet[i:]
            uuid, pckt = ParseUUID(pckt, consume=True)
            length = pckt[0]
            pckt = pckt[1:]
            name = ParseString(pckt, length)
            self.names[uuid] = name

    def _player_action_four(self, count, packet):
        for i in range(int(len(packet)/count)):
            pckt = packet[i:]
            uuid, pckt = ParseUUID(pckt, consume=True)
            with self.lock:
                entities = self.entities
                if uuid in self.names:
                    self.names.pop(uuid)
                for entity in entities:
                    if entities[entity]["uuid"] == uuid:
                        del self.entities[entity]

    def handle_PlayerInfo(self, packet):
        action, packet = ParseVarInt(packet, consume=True)
        number_of_players, packet = ParseVarInt(packet, consume=True)
        if number_of_players:
            players = int(len(packet) / number_of_players)
            if action == 0:
                self._player_action_zero(players, packet)
            elif action == 1:
                # this is game mode
                pass
            elif action == 2:
                # this is ping info
                pass
            elif action == 4:
                self._player_action_four(players, packet)
            else:
                print("Play.PlayerInfo")
                print(action)
                hex_print(packet)
        return []

    def handle_SpawnPlayer(self, packet):
        entity_id, packet = ParseVarInt(packet, consume=True)
        uuid, packet = ParseUUID(packet, consume=True)
        x, packet = ParseDouble(packet, consume=True)
        y, packet = ParseDouble(packet, consume=True)
        z, packet = ParseDouble(packet, consume=True)
        with self.lock:
            self.entities[entity_id] = {'position': [x, y, z], 'uuid': uuid}
        return []

    def handle_EntityMetadata(self, packet):
        """TODO"""
        # print("Play.EntityMetadata")
        return []

    def handle_EntityProperties(self, packet):
        entity_id, packet = ParseVarInt(packet, consume=True)
        number_of_properties, packet = ParseInt(packet, consume=True)
        stats = []
        for _ in range(number_of_properties):
            key_len = packet[0]
            key, packet = ParseString(packet[1:], key_len, consume=True)
            value, packet = ParseDouble(packet, consume=True)
            number_of_mods, packet = ParseVarInt(packet, consume=True)
            mods = []
            for _ in range(number_of_mods):
                uuid, packet = ParseUUID(packet, consume=True)
                amount, packet = ParseDouble(packet, consume=True)
                operation = packet[0]
                packet = packet[1:]
                mods.append([uuid, amount, operation])
            mod_amount = 0
            for mod in mods:
                uuid, amount, operation = mod
                del uuid
                if operation == 0:
                    mod_amount += amount
                else:
                    print("Play.EntityProperties: ", operation, amount)
            value += mod_amount
            stats.append((key, value))
        
        with self.lock:
            if entity_id in self.entities:
                self.entities[entity_id]["properties"] = stats
                if "name" not in self.entities[entity_id]:
                    self.entities[entity_id]["name"] = self.names[self.entities[entity_id]["uuid"]]

        return packet

    def handle_PlayerPositionAndLook(self, packet):
        x, packet = ParseDouble(packet, consume=True)
        y, packet = ParseDouble(packet, consume=True)
        z, packet = ParseDouble(packet, consume=True)
        yaw, packet = ParseFloat(packet, consume=True)
        pitch, packet = ParseFloat(packet, consume=True)
        # Instead of parsing flags we just skip a byte
        # flags, packet = ParseByte(packet, consume=True)
        packet = packet[1:]
        teleport_id, packet = ParseVarInt(packet, consume=True)
        # print("Play.PlayerPositionAndLook (x:%s, y:%s, z:%s, teleport:%s)" % (x, y, z, teleport_id))
        self.position = [x, y, z]
        self.pitch = pitch
        self.yaw = yaw
        self.send_TeleportConfirm(teleport_id)
        return packet

    def handle_WorldBorder(self, packet):
        """TODO"""
        # print("Play.WorldBorder")
        return []

    def handle_TimeUpdate(self, packet):
        """TODO"""
        # print("Play.TimeUpdate")
        return []

    def handle_SpawnPosition(self, packet):
        """TODO"""
        position, packet = ParseLong(packet, consume=True)
        x, y, z = ParseCoords(position)
        # print("Play.SpawnPosition (x:%s, y:%s, z:%s)" % (x, y, z))
        # self.position = [x, y, z]
        return []

    def handle_KeepAlive(self, packet):
        # print("Play.KeepAlive")
        self.send_KeepAlive(packet)
        return []

    def send_KeepAlive(self, packet):
        # print("Sending KeepAlive")
        packet = PackVarInt(0x0e) + packet
        self.send(packet)

    def handle_Disconnect(self, packet):
        print("Play.Disconnect")
        import sys; sys.exit(-1)
        return []

    def handle_EntityRelativeMove(self, packet):
        entity_id, packet = ParseVarInt(packet, consume=True)
        delta_x, packet = ParseShort(packet, consume=True)
        delta_y, packet = ParseShort(packet, consume=True)
        delta_z, packet = ParseShort(packet, consume=True)
        # Not handling on_ground
        packet = packet[1:]
        # Calculating relative changes to coords
        with self.lock:
            if entity_id in self.entities and self.entities[entity_id]["position"]:
                x, y, z = self.entities[entity_id]["position"]
                div = (32*128)
                delta_x = delta_x / div
                delta_y = delta_y / div
                delta_z = delta_z / div
                new_x = x + delta_x
                new_y = y + delta_y
                new_z = z + delta_z
                self.entities[entity_id]["position"] = [new_x, new_y, new_z]
    
        # print("Play.EntityRelativeMove (%s: x:%s, y:%s, z:%s)" % (entity_id, x, y, z))
        return []

    def handle_EntityLookAndRelativeMove(self, packet):
        self.handle_EntityRelativeMove(packet)
        return []

    def handle_WindowItems(self, packet):
        """TODO"""
        # print("Play.WindowItems")
        return []

    def handle_Advancements(self, packet):
        """TODO"""
        # print("Play.Advancements")
        return []

    def handle_SetSlot(self, packet):
        """TODO"""
        # print("Play.SetSlot")
        return []

    def handle_UpdateHealth(self, packet):
        print("Play.UpdateHealth")
        self.respawn()
        return []

    def handle_BlockChange(self, packet):
        """TODO"""
        print("Play.BlockChange")
        return []

    def handle_SetExperience(self, packet):
        """TODO"""
        # print("Play.SetExperience")
        return []

    def handle_EntityTeleport(self, packet):
        entity_id, packet = ParseVarInt(packet, consume=True)
        x, packet = ParseDouble(packet, consume=True)
        y, packet = ParseDouble(packet, consume=True)
        z, packet = ParseDouble(packet, consume=True)
        # Not handling yaw, pitch, or on_ground
        packet = packet[4:]
        
        with self.lock:
            if entity_id not in self.entities:
                self.entities[entity_id] = {"position": []}
            self.entities[entity_id]["position"] = [x, y, z]

        return packet

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
            #print("Unknown packet ID %s for state %s" % (hex(packet_id), self.state))
            pass

        try:
            func = getattr(self, "handle_" + packet_id.split(".")[1])
            packet = func(packet=packet)
            assert len(packet) == 0
        except AttributeError:
            # print("Unknown packet: %s" % packet)
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

    def send_TeleportConfirm(self, teleport_id):
        """Teleport Confirm"""
        print("Sending Server TeleportConfirm")
        packet = PackVarInt(0x00) + PackVarInt(teleport_id)
        self.send(packet)
        self.accepted_teleport = teleport_id

    def send_PlayerPosition(self, x, y, z):
        self.position = [x, y, z]
        # y = y - 1.62
        packet = PackVarInt(0x10) + PackDouble(x) + PackDouble(y) + PackDouble(z) + PackBool(True)
        self.send(packet)

    def send_PlayerLook(self, yaw, pitch):
        """Look at something"""
        packet = PackVarInt(0x12) + PackFloat(yaw) + PackFloat(pitch) + PackBool(True)
        self.send(packet)

    def send_PlayerPositionAndLook(self, x, y, z, yaw, pitch):
        self.position = [x, y, z]
        packet = PackVarInt(0x11) + PackDouble(x) + PackDouble(y) + PackDouble(z) + PackFloat(yaw) + PackFloat(pitch) + PackBool(True)
        self.send(packet)

    # send_UseEntity
    def attack(self, name):
        with self.lock:
            entities = copy.deepcopy(self.entities)
        
        for entity in entities:
            if "name" in entities[entity] and entities[entity]["name"] == name:
                # 0: interact, 1: attack, 2: interact
                packet = PackVarInt(0x0d) + PackVarInt(entity) + PackVarInt(1)
                self.send(packet)

    def respawn(self):
        self.send_ClientStatus(0)

    def jiggle(self, x, y):
        del x, y
        return
        while True:
            x, y, z = self.position
            if y > 4:
                y = y - 1
            move = 10
            x = x - move
            sleep = 0.5
            time.sleep(sleep)
            self.send_PlayerPosition(x, y, z)
            y = y + move
            time.sleep(sleep)
            self.send_PlayerPosition(x, y, z)
            x = x + move
            time.sleep(sleep)
            self.send_PlayerPosition(x, y, z)
            y = y - move
            time.sleep(sleep)
            self.send_PlayerPosition(x, y, z)

    def follow(self, name):
        def new_position(target, own):
            if int(target) > int(own):
                val = own + 1
            elif int(target) < int(own):
                val = own - 1
            else:
                val = own
            return val

        while True:
            with self.lock:
                entities = copy.deepcopy(self.entities)

            for entity_id in entities:
                entity = entities[entity_id]
                if "name" in entity and entity["name"] == name:
                    target_x, target_y, target_z = entity["position"]
                    own_x, own_y, own_z = self.position
                    x = new_position(target_x, own_x)
                    y = new_position(target_y, own_y)
                    z = new_position(target_z, own_z)
                    yaw, pitch = self.calculate_yaw_and_pitch(target_x, target_y, target_z)
                    self.send_PlayerPositionAndLook(x, y, z, yaw, pitch)
                    self.attack(name)
                    time.sleep(0.1)

    def run(self):
        print("MCBot running...")
        self.send_HandShake()
        self.send_LoginStart()
        jiggling = False

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

                    # Now that we have the packet handle it
                    try:
                        self.handle_packet(packet)
                    except:
                        print("FAIL: ", "".join([chr(x) for x in packet]))
                        self.handle_packet(packet)
                    packet = []

            if self.position and self.accepted_teleport and not jiggling:
                jiggling = True
                # _thread.start_new_thread(self.jiggle, (0, 0, ))
                _thread.start_new_thread(self.follow, ("top1_", ))
                
