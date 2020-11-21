"""Minecraft bot"""
import argparse
import struct
import libmc
from configparser import ConfigParser
import _thread

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
    parser = argparse.ArgumentParser(description='MCBot.')
    parser.add_argument('name', help="name of the bot")

    args = parser.parse_args()
    mc = setup_bot(args.name)
    mc.run()

if __name__ == "__main__":
    main()