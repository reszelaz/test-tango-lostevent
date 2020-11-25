import time
import threading

import tango
from tango.server import Device, attribute, command


class DeviceLostEvent(Device):

    def init_device(self):
        self.set_change_event("state", True, False)
        self.set_state(tango.DevState.ON)

    def is_cmd_allowed(self):
        return self.get_state() == tango.DevState.ON

    @command()
    def cmd(self):
        self.set_state(tango.DevState.MOVING)
        self.push_change_event("state")

        def job(device):
            time.sleep(0.1)
            self.set_state(tango.DevState.ON)
            self.push_change_event("state")

        threading.Thread(target=job, args=(self, )).start()


if __name__ == "__main__":
    DeviceLostEvent.run_server()
