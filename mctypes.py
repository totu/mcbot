"""MC types"""
import struct 
import uuid

def hex_print(packet):
    print([hex(x) if isinstance(x, int) else hex(ord(x)) for x in packet])

def PackVarInt(value):
    result = []
    for i in range(5):
        number = value >> 7 * i 
        if number & ~0x7f != 0:
            result.append((number & 0x7f) + 0x80)
        else:
            result.append(number & 0x7f)
            break
    return [chr(x) for x in result]

def ParseVarInt(packet, consume=False):
    result = 0
    for i in range(5):
        read = packet[i]
        value = read & 0b011111111
        result |= (value & 0x7f) << 7 * i

        if read & 0b10000000 == 0:
            break

    # If consume is set only return remaining packet
    if consume:
        return result, packet[i+1:]

    return result

def PackString(str):
    return PackVarInt(len(str)) + [x for x in str]

def ParseString(packet, length, consume=False):
    string = "".join([chr(x) for x in packet[:length]])
    if consume:
        return string, packet[length:]
    return string

def PackUnsignedShort(value):
    return [chr(x) for x in struct.pack(">h", value)]

def ParseShort(packet, consume=False):
    packet = [ord(x) if isinstance(x, str) else x for x in packet]
    value = struct.unpack(">h", bytes(packet[:2]))[0]
    if consume:
        return value, packet[2:]
    return value 

def ParseInt(packet, consume=False):
    packet = [ord(x) if isinstance(x, str) else x for x in packet]
    value = struct.unpack(">i", bytes(packet[:4]))[0]
    if consume:
        return value, packet[4:]
    return value 

def ParseDouble(packet, consume=False):
    packet = [ord(x) if isinstance(x, str) else x for x in packet]
    value = struct.unpack(">d", bytes(packet[:8]))[0]
    if consume:
        return value, packet[8:]
    return value 

def PackDouble(value):
    return [chr(x) for x in struct.pack(">d", value)]

def ParseBool(packet, consume=False):
    packet = [ord(x) if isinstance(x, str) else x for x in packet]
    value = struct.unpack(">?", bytes(packet[0]))[0]
    if consume:
        return value, packet[1:]
    return value 

def PackBool(boolean):
    return [chr(x) for x in struct.pack(">?", boolean)]

def ParseFloat(packet, consume=False):
    packet = [ord(x) if isinstance(x, str) else x for x in packet]
    value = struct.unpack(">f", bytes(packet[:4]))[0]
    if consume:
        return value, packet[4:]
    return value 

def ParseByte(packet, consume=False):
    assert False, "this is still bad and you should feel bad"
    value = struct.unpack(">b", bytes(packet[0]))
    if consume:
        return value, packet[1:]
    return value

def ParseLong(packet, consume=False):
    packet = [ord(x) if isinstance(x, str) else x for x in packet]
    value = struct.unpack(">q", bytes(packet))[0]
    if consume:
        return value, packet[8:]
    return value 

def PackLong(value):
    packet = [chr(x) for x in struct.pack(">q", value)]
    return packet

def ParseCoords(value):
    x = value >> 38
    y = value & 0xfff
    z = ((value & 0x3ffffff000) << 26) >> 38
    if x >= 2**25:
        x = x - 2**26
    if y >= 2**11:
        y = y - 2**12
    if z >= 2**25:
        z = z - 2**26
    return x, y, z

def PackCoords(x, y, z):
    value = ((int(x) & 0x3FFFFFF) << 38) | ((int(z) & 0x3FFFFFF) << 12) | (int(y) & 0xFFF)
    packet = PackLong(value)
    return packet

def ParseUUID(packet, consume=False):
    string = uuid.UUID(bytes=bytes(packet[:16]))
    if consume:
        return string, packet[16:]
    return string

if __name__ == "__main__":
    assert 129 == ParseVarInt([ord(x) for x in PackVarInt(129)])
    assert 128 != ParseVarInt([ord(x) for x in PackVarInt(129)])
    assert 172 == ParseVarInt([ord(x) for x in PackVarInt(172)])
    assert 9005 == ParseVarInt([ord(x) for x in PackVarInt(9005)])
    x, y, z = ParseCoords(PackCoords(1,1,1)[0])
    assert x == 1 and y == 1 and z == 1
    x, y, z = ParseCoords(PackCoords(-500,-300,-1000)[0])
    assert x == -500 and y == -300 and z == -1000
    x, y, z = ParseCoords(PackCoords(620, 1200, 34000)[0])
    assert x == 620 and y == 1200 and z == 34000
    assert 123 == ParseLong(PackLong(123))
    assert 4223720368477807 == ParseLong(PackLong(4223720368477807))