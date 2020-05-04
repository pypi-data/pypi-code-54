import socket, sys

HOST = "127.0.0.1"
PORT = 4040


def main() -> None:
    """Connect to given server and get bot health"""
    print("inside main", sys.argv)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)

    if data == b"healthy":
        print("Healthy!")
    else:
        print(":(")


if __name__ == "__main__":
    print("name is main", sys.argv)
    main()
