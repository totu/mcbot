"""libmc handlers"""
from mctypes import ParseVarInt, ParseString, ParseUUID, ParseDouble, ParseFloat, ParseShort, ParseInt, ParseLong, ParseCoords
from enums import Play
from helpers import hex_print
import zlib

class Handler():
    def __init__(self):
        self.lock = None
        self.entities = []
        self.names = []
        self.sock = None

    def recv(self, count):
        return self.sock.recv(count)

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
            # pylint: disable=not-context-manager
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
        # pylint: disable=not-context-manager
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
        
        # pylint: disable=not-context-manager
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
        # pylint: disable=no-member
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
        # pylint: disable=no-member
        self.send_KeepAlive(packet)
        return []

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
        # pylint: disable=not-context-manager
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
        # pylint: disable=no-member
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
        
        # pylint: disable=not-context-manager
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
