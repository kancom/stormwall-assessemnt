import json
import socket
from time import sleep

data = (
    (
        {"A1": 1, "A2": 10, "A3": 100},
        {"A1": 2, "A2": 12, "A3": 102},
        {"A1": 3, "A2": 30, "A3": 130},
    ),
    (
        {"A1": 4, "A2": 20, "A3": 200},
        {"A1": 5, "A2": 13, "A3": 103},
        {"A1": 6, "A2": 40, "A3": 140},
    ),
    ({"A1": 6, "A2": 40, "A3": 140},),
)

host = "127.0.0.1"
port = 8000


def test_e2e():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for chunk in data:
        for l in chunk:
            udp_socket.sendto(json.dumps(l).encode("utf-8"), (host, port))
        sleep(11)
    udp_socket.close()
