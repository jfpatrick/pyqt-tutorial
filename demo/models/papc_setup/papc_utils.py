import time
import datetime
from threading import Event, Thread

from papc.device import Device


class IntervalUpdateDevice(Device):
    """
        Subclass of ``Device`` that updates one of its fields at a specified frequency.
        You can subclass ``Device`` to implement any behavior you might want to simulate.
    """
    def __init__(self, field_to_update, selector_to_update, frequency=30, *args, **kwargs):
        # Take out the `frequency` argument from the kwargs, or default to 30Hz
        self.field_to_update = field_to_update
        self.selector_to_update = selector_to_update
        super().__init__(*args, **kwargs)
        # Start the internal timer (RepeatedTimer is defined below)
        self.timer = RepeatedTimer(1 / frequency, self.time_tick)

    def time_tick(self):
        """ Callback executed at each tick of the timer """
        now = datetime.datetime.now()
        t = time.mktime(now.timetuple()) + now.microsecond / 1e6
        # Set the given field with the current timestamp
        self.set_state({self.field_to_update: t}, self.selector_to_update)


class RepeatedTimer:
    """
    Implementation of a recurrent timer, that keeps calling a given function
    at a given frequency. Can be stopped, paused and resumed.
    Arguments can be passed to the target function by passing them
    as extra arguments to the ``__init__`` function of this timer.
    """
    def __init__(self, interval, function, *args, **kwargs):
        self.interval = interval
        self.function = self._orig_function = function
        self.args = args
        self.kwargs = kwargs
        self.start = time.time()
        self.event = Event()
        self.thread = Thread(target=self._target)
        self.thread.daemon = True
        self.thread.start()

    def _target(self):
        while not self.event.wait(self._time):
            self.function(*self.args, **self.kwargs)

    @property
    def _time(self):
        return self.interval - ((time.time() - self.start) % self.interval)

    def pause(self):
        self.function = lambda *args, **kwargs: None

    def resume(self):
        self.function = self._orig_function

    def stop(self):
        self.event.set()
        self.thread.join()
