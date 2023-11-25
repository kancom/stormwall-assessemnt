import multiprocessing as mp

from stormwall.wiring import container

if __name__ == "__main__":
    ports = list(map(int, container.settings.listen_ports.split(",")))
    master = mp.Process(target=container.master, args=(container.queue,))
    master.start()
    workers = [
        mp.Process(target=container.worker, args=(container.queue, p)) for p in ports
    ]
    for w in workers:
        w.start()
    master.join()
    for w in workers:
        w.join()
