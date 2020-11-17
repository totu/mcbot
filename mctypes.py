"""MC types"""
import struct 

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
        return string, packet[length+1:]
    return string

def PackUnsignedShort(value):
    return [chr(x) for x in struct.pack(">h", value)]

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
    value = ((x & 0x3FFFFFF) << 38) | ((z & 0x3FFFFFF) << 12) | (y & 0xFFF)
    packet = PackLong(value)
    return packet

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