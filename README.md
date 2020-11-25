# Demo a bug in (Py)Tango with lost event? 

Example to reproduce a lost event when executing in parallel
subscription/unsubscription to one attribute's events and listening to other
attribute events.

The architecture is as following. We have one DS called `DeviceLostEvent`
which exports one device of the `DeviceLostEvent` class. This device has one
command `cmd` which when executed change's device state to MOVING and pushes
the state event. Just after that it starts a thread which will sleep a little
and again change and push state to ON.

The client starts a `long_job()` in a thread which will continuously execute
the command based on the events being received. Then it continuous in the main
thread to execute `short_job()` which will subscribe and unsubscribe to another
attribute's events. The `long_job()` stops receiving events after exactly 500
iterations!

To demonstrate that the event is pushed by the server and it is just this client
which stops receiving the events I run in parallel an ipython session which
listens to the state events as well. There we can see that the event was
actually pushed.

## Steps to reproduce the problem
1. Register in Tango Database one DeviceServer DS with instance name `test`
   with 1 device of `DeviceLostEvent` class, with the name
   `test/devicelostevent/1`.
   ```console
   tango_admin --add-server DeviceLostEvent/test DeviceLostEvent test/devicelostevent/1    
   ```
2. Start device server:
   ```console
   python3 DeviceLostEvent.py test`
   ```
3. Start a secondary ipython client to listen to the events:
   ```
   import tango
   d = tango.DeviceProxy("test/devicelostevent/1")
   d.subscribe_event("state", tango.EventType.CHANGE_EVENT, tango.utils.EventCallback())
   ```
4. Start our client:
   ```console
   python3 client.py`
   ```
5. Wait until 500 iteration...
