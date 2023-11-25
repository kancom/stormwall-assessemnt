import multiprocessing as mp
import socket

import ujson as json


def worker(_, queue: mp.Queue, port: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", port))

    while True:
        data, _ = sock.recvfrom(1024)
        try:
            message = json.loads(data.decode())
            queue.put(message)
        except json.JSONDecodeError:
            pass
