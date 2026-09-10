"""
app/polling/poller.py
"""
from datetime import timedelta
from threading import Event, Thread
from queue import Queue, Full

from app.polling.events import SensorCheckEvent


class SensorPoller:
    """
    Periodically signals a sensor check
    """
    def __init__(self, event_queue: Queue, interval: timedelta):
        self._event_queue = event_queue
        self._interval = interval
        self._pending = Queue(maxsize=1)
        self._stop = Event()

    def start(self) -> Thread:
        """
        Start polling sensors
        """
        thread = Thread(target=self._run, daemon=True)
        thread.start()
        return thread

    def stop(self) -> None:
        """
        Stop polling sensors
        """
        self._stop.set()

    def mark_processed(self) -> None:
        """
        Called once the consumer finishes handling a `SensorCheckEvent`,
        freeing the next tick to fire
        """
        self._pending.get_nowait()

    def _run(self) -> None:
        while not self._stop.wait(self._interval.total_seconds()):
            try:
                self._pending.put_nowait(True)
            except Full:
                return
            self._event_queue.put(SensorCheckEvent())
