"""helpers"""
import math

def hex_print(packet):
    print([hex(x) if isinstance(x, int) else hex(ord(x)) for x in packet])

def calculate_yaw_and_pitch(target_coords, own_coords):
    try:
        dx, dy, dz = [d[0] - d[1] for d in zip(target_coords, own_coords)]
        # x0, y0, z0 = own_coords
        # x, y, z = target_coords
        # dx = x-x0
        # dy = y-y0
        # dz = z-z0
        r = math.sqrt(dx*dx + dy*dy + dz*dz)
        yaw = -math.atan2(dx,dz)/math.pi*180
        if yaw < 0:
            yaw = 360 + yaw
        pitch = -math.asin(dy/r)/math.pi*180
    except ZeroDivisionError:
        return None, None

    return yaw, pitch
