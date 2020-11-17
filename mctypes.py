"""MC types"""
import struct 

def PackVarInt(_int):
    result = []
    for i in range(5):
        number = _int >> 7 * i 
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

def PackUnsignedShort(_int):
    return [chr(x) for x in struct.pack(">h", _int)]

def ParseLong(packet, consume=False):
    _long = struct.unpack(">q", bytes(packet))[0]
    if consume:
        return _long, packet[8:]
    return _long 

if __name__ == "__main__":
    assert 129 == ParseVarInt([ord(x) for x in PackVarInt(129)])
    assert 128 != ParseVarInt([ord(x) for x in PackVarInt(129)])
    assert 172 == ParseVarInt([ord(x) for x in PackVarInt(172)])
    assert 9005 == ParseVarInt([ord(x) for x in PackVarInt(9005)])