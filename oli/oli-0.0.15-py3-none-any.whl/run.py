import platform
import signal
import sys
from macos.mac import run as rerun

def signal_handler(signal, frame):
    print("\nGracefully exiting")
    sys.exit(0)

def main():
    platform_name = platform.system()
    if platform_name == "Darwin":
        rerun()
        

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    print("hello")
    main()

