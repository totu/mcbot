import _thread
import time
import socket
import copy
from mctypes import ParseVarInt, PackVarInt
from enums import Play, Login
from handlers import Handler
from senders import Sender
from helpers import calculate_yaw_and_pitch


class libmc(Handler, Sender):
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
        self.yaw = 0
        self.pitch = 0
        self.accepted_teleport = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.lock = _thread.RLock()
        self.following = None
        print("MCBot initialized")

    def attack(self, name):
        """send_UseEntity"""
        print("MCBot attacking:", name)
        distance = 3
        with self.lock:
            entities = copy.deepcopy(self.entities)

        for entity in entities:
            ent = entities[entity]
            if ent.is_name(name) and ent.is_inrange(self.position, distance):
                # Jump for crit
                x, y, z = self.position
                self.send_PlayerPositionAndLook(
                    x, y + 0.5, z, self.yaw, self.pitch, on_ground=False
                )
                time.sleep(0.05)
                self.send_PlayerPositionAndLook(
                    x, y + 1, z, self.yaw, self.pitch, on_ground=False
                )
                time.sleep(0.05)
                self.send_PlayerPositionAndLook(
                    x, y, z + 0.5, self.yaw, self.pitch, on_ground=False
                )
                time.sleep(0.05)
                # 0: interact, 1: attack, 2: interact
                packet = PackVarInt(0x0D) + PackVarInt(entity) + PackVarInt(1)
                self.send(packet)
                # animation
                packet = PackVarInt(0x27) + PackVarInt(0)
                self.send(packet)
                # land?
                time.sleep(0.05)
                self.send_PlayerPositionAndLook(
                    x, y, z, self.yaw, self.pitch, on_ground=True
                )

    def respawn(self):
        self.send_ClientStatus(0)

    def jiggle(self, x, y):
        del x, y
        return

    def follow(self, name, cmd):
        print("MCBot following:", name)

        def new_position(target, own, move=1):
            if int(target) > int(own):
                val = own + move
            elif int(target) < int(own):
                val = own - move
            else:
                val = own
            return val

        while True:
            if not self.following:
                break

            with self.lock:
                entities = copy.deepcopy(self.entities)

            for entity_id in entities:
                entity = entities[entity_id]

                if entity.is_name(name, partial=True):
                    own_pos = self.position
                    target_pos = entity.position
                    x, y, z = [
                        new_position(x[0], x[1]) for x in zip(target_pos, own_pos)
                    ]

                    # dont change height if within limit
                    if abs(y - self.position[1]) < 2:
                        y = self.position[1]

                    yaw, pitch = calculate_yaw_and_pitch(target_pos, own_pos)

                    # move towards the target
                    if entity.is_not_inrange(own_pos, 2):
                        self.send_PlayerPositionAndLook(x, y, z, yaw, pitch)

                    # try to stick to land
                    elif target_pos[1] < own_pos[1]:
                        self.send_PlayerPositionAndLook(
                            own_pos[0], target_pos[1], own_pos[2], yaw, pitch
                        )

                    self.attack(entity.name)

    def bot_command(self, command):
        command = command.strip()
        print("MCBot got command:", command)
        if command.startswith("stop"):
            self.following = None

        if command.startswith("follow:") or command.startswith("kill:"):
            cmd, name = command.split(":")
            self.following = None
            time.sleep(0.3)
            self.following = _thread.start_new_thread(
                self.follow,
                (
                    name,
                    cmd,
                ),
            )
            # _thread.start_new_thread(self.jiggle, (0, 0, ))

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
                    length = ParseVarInt(packet)

                    # Hack to make sure socket gets all bytes
                    packet = []
                    while len(packet) < length:
                        packet.append(self.recv(1)[0])
                    assert (
                        len(packet) == length
                    ), "Length is somehow different! (%s != %s)" % (len(packet), length)

                    # Now that we have the packet handle it
                    try:
                        self.handle_packet(packet)
                    except:
                        print("FAIL: ", "".join([chr(x) for x in packet]))
                        self.handle_packet(packet)
                    packet = []
