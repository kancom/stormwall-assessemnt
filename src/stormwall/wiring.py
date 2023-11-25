import multiprocessing as mp

from stormwall.master import Master
from stormwall.settings import Settings
from stormwall.worker import worker


class Container:
    queue = mp.Queue()
    settings = Settings()
    master = Master(
        intervals=list(map(int, settings.intervals.split(","))),
        sync_interval=settings.sync_interval,
        output=settings.output_file,
    )
    worker = worker


container = Container()
