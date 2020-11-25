import time
import threading

import tango


def short_job(dev):
    print("Starting short_job")

    def cb(*args):
        pass

    id_ = dev.subscribe_event("state", tango.EventType.CHANGE_EVENT, cb)
    try:
        time.sleep(0.01)
    finally:
        dev.unsubscribe_event(id_)


def long_job(dev_name):
    with tango.EnsureOmniThread():
        dev = tango.DeviceProxy(dev_name)
        state = None
        state_event = threading.Event()

        def state_cb(event):
            nonlocal state
            state = event.attr_value.value
            print("received state: {}".format(state))
            state_event.set()

        def exec_cmd():
            state_event.clear()
            dev.cmd()
            print("waiting for state == MOVING")
            state_event.wait()
            state_event.clear()
            if state != tango.DevState.MOVING:
                raise RuntimeError(
                    "state is: {} but expecting MOVING".format(state))
            print("waiting for state == ON")
            state_event.wait()
            if state != tango.DevState.ON:
                raise RuntimeError(
                    "state is: {} but expecting ON".foramt(state))

        dev.subscribe_event("state", tango.EventType.CHANGE_EVENT, state_cb)
        i = 0
        while True:
            print("Iteration {}".format(i))
            exec_cmd()
            i += 1


if __name__ == "__main__":
    t = threading.Thread(target=long_job, args=("test/devicelostevent/1",))
    t.start()
    with tango.EnsureOmniThread():
        dev = tango.DeviceProxy('sys/tg_test/1')
        while True:
            short_job(dev)
