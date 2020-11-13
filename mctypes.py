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

def ParseVarInt(sock):
    result = 0
    for i in range(5):
        read = ord(packet[i])
        value = read & 0b011111111
        result += value << 7 * i

        if read & 0b10000000 == 0:
            break
    return result


def PackString(str):
    return PackVarInt(len(str)) + [x for x in str]

def PackUnsignedShort(_int):
    return [chr(x) for x in struct.pack(">h", _int)]


if __name__ == "__main__":
    print("pack")
    print(127, PackVarInt(127))
    print(128, PackVarInt(128))
    print(129, PackVarInt(129))
    print("read")
    print(127, ParseVarInt(PackVarInt(127)))
    print(128, ParseVarInt(PackVarInt(128)))
    print(129, ParseVarInt(PackVarInt(129)))
    print("string")
    print(PackString("127.0.0.1"))
    print(PackString("0"))
    print("port")
    print(PackUnsignedShort(26655))
    print(PackUnsignedShort(22))