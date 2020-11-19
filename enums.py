"""Enums for libmc"""
from enum import Enum

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
    ChatMessage = 0x0e