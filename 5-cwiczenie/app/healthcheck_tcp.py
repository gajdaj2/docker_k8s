import socket
import sys


def main() -> int:
    if len(sys.argv) != 3:
        print("Uzycie: python healthcheck_tcp.py <host> <port>")
        return 1

    host = sys.argv[1]
    port = int(sys.argv[2])

    try:
        with socket.create_connection((host, port), timeout=2):
            return 0
    except OSError:
        return 1


if __name__ == "__main__":
    sys.exit(main())
