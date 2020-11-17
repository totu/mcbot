"""Minecraft bot"""
import struct
import libmc
from configparser import ConfigParser

# Main loop
def setup_bot(name):
    config = ConfigParser()
    config.read('conf')
    host = config.get('server', 'ip')
    port = int(config.get('server', 'port'))
    lib = libmc.libmc(name, host, port)
    return lib

def main():
    """do the thing"""
    mc = setup_bot("top2_")
    mc.run()

if __name__ == "__main__":
    main()