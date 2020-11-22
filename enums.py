"""Enums for libmc"""
from enum import Enum


class Login(Enum):
    Disconnect = 0x00
    EncryptionRequest = 0x01
    LoginSuccess = 0x02
    SetCompression = 0x03


class Play(Enum):
    Advancements = 0x51
    BlockChange = 0x0B
    ChatMessage = 0x0E
    ChunkData = 0x22
    CloseWindow = 0x13
    DeclareCommands = 0x11
    DeclareRecipes = 0x54
    Disconnect = 0x1B
    EntityLookAndRelativeMove = 0x29
    EntityMetadata = 0x3F
    EntityProperties = 0x52
    EntityRelativeMove = 0x28
    EntityStatus = 0x1C
    EntityTeleport = 0x50
    HeldItemChange = 0x3D
    JoinGame = 0x25
    KeepAlive = 0x21
    PlayerAbilities = 0x2E
    PlayerInfo = 0x30
    PlayerPositionAndLook = 0x32
    PluginMessage = 0x19
    ServerDifficulty = 0x0D
    SetExperience = 0x43
    SetSlot = 0x17
    SpawnPlayer = 0x05
    SpawnPosition = 0x49
    Tags = 0x55
    TimeUpdate = 0x4A
    UnlockRecipes = 0x34
    UpdateHealth = 0x44
    WindowItems = 0x15
    WorldBorder = 0x3B
