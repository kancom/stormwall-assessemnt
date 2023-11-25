import multiprocessing as mp
import queue as queue_mod
import time
from typing import List

data = {}


class Master:
    def __init__(self, intervals: List[int], sync_interval: int, output: str):
        self._f = None
        self._intervals = intervals
        self._sync_interval = sync_interval
        self._output = output

    def _sync_data(self, data: dict):
        if self._f is None:
            self._f = open(self._output, "a+")
        lines = []
        for k, v in data.items():
            for ik, iv in v.items():
                lines.append(
                    f'"timestamp":{ik}, "count_type":"{k}s", "A1_sum": {iv["A1_sum"]}, "A2_max":{iv["A2_max"]}, "A3_min":{iv["A3_min"]}\n'
                )
            data[k] = {}
        self._f.writelines(lines)

    def __call__(self, queue: mp.Queue):
        self._queue = queue
        for interval in self._intervals:
            data[interval] = {}
        sync_ts = time.time()

        while True:
            try:
                message = self._queue.get(timeout=1)
                times = time.time()
                timestamp = int(times)

                for interval in self._intervals:
                    ts = timestamp // interval * interval

                    print(ts in data[interval], times - sync_ts, self._sync_interval)
                    if ts not in data[interval]:
                        if times - sync_ts > self._sync_interval:
                            self._sync_data(data)
                            sync_ts = times
                        data[interval][ts] = {
                            "A1_sum": 0,
                            "A2_max": float("-inf"),
                            "A3_min": float("inf"),
                        }
                    data[interval][ts]["A1_sum"] += message["A1"]
                    data[interval][ts]["A2_max"] = max(
                        data[interval][ts]["A2_max"], message["A2"]
                    )
                    data[interval][ts]["A3_min"] = min(
                        data[interval][ts]["A3_min"], message["A3"]
                    )

            except queue_mod.Empty:
                pass
