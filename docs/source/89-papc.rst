.. index:: Testing with ``papc``
.. index:: ``papc``
.. _papc:

=================
Testing with papc
=================

``papc`` is a pure Python library that is designed to mimic PyJAPC devices for simulation and testing purposes.

It provides the same exact API provided by PyJAPC and, as such, PyJAPC instances can be monkey-patched
(i.e. replaced at runtime) with ``papc`` object that do not really connect to the control system, but mimic it
to a great degree.

``papc`` is perfect for building sandboxes for expert applications, to perform tests on GitLab CI, and to run
expert apps in simulated mode on non TN-enabled machines.

.. warning:: ``papc`` is still in Beta stage. Some functionality may be missing or buggy. If you encounter a bug,
    contact Acc-Py for support.

.. index:: How ``papc`` works
.. _papc_how_it_works:

How it works
============
``papc`` offers a PyJAPC compatible interface, that you can use to connect your application to the simulated
devices. Such interface can be created with the help of the ``SimulatedPyJapc`` object::

    from papc.interfaces.pyjapc import SimulatedPyJapc

    mocked_pyjapc = SimulatedPyJapc.from_simulation_factory(<factory_method>)

This method takes in input a function ``factory_method`` that must return a ``System`` object. For example::

    from papc.interfaces.pyjapc import SimulatedPyJapc
    from papc.system import System

    my_system = System(devices=list_of_devices)
    mocked_pyjapc = SimulatedPyJapc.from_simulation_factory(lambda: my_system)

As you can see, ``System`` objects must be intialized with a ``list_of_devices``.
Such devices are mocks of the real devices our app wants to connect to.

Let's see what ``list_of_devices`` contains. Here is the function creating it::

    import pyjapc
    <other pyqt imports>

    from papc.interfaces.pyjapc import SimulatedPyJapc
    from papc.system import System

    from papc.device import Device
    from papc.fieldtype import FieldType, EquationFieldType
    from papc.deviceproperty import Acquisition, Setting, Command
    from papc.simulator.trig import RepeatedTimer
    from papc.timingselector import TimingSelector


    # Modified from https://gitlab.cern.ch/pelson/papc/blob/master/papc/simulator/trig.py
    class IntervalUpdateDevice(Device):
        """
            Device subclass with a timer. It updates the specified fields/selectors pairs at the desired frequency.
            set_fields_selectors is a list of tuples (propertyName#fieldName, TimingSelector("selector"))
        """
        def __init__(self, set_fields_selectors: List[Tuple[str, str]]=[], *args, **kwargs):
            freq_hz = kwargs.pop('frequency', 30)
            super().__init__(*args, **kwargs)
            self.timer = RepeatedTimer(1 / freq_hz, self.time_tick)
            # set_fields_selectors is a list of tuples (propertyName#fieldName, TimingSelector("selector"))
            self.set_fields_selectors = set_fields_selectors

        def time_tick(self):
            now = datetime.datetime.now()
            t = time.mktime(now.timetuple()) + now.microsecond / 1e6
            for field_selector_pair in self.set_field_selector:
                self.set_state({field_selector_pair[0]: t}, field_selector_pair[1])


    def setup_papc_simulation():
        # List containing all your mocked devices
        my_list_of_devices: List[Device] = []

        # List of the properties and fields of your first mocked device
        first_device_properties = (
            Setting('SystemStatus', (
                FieldType("status", "int", initial_value=1),
                FieldType("name", "str", initial_value="My System"),
                FieldType("my_parameter", "float", initial_value=0)
            )),
            Acquisition('SystemData', (
                EquationFieldType('sin_of_my_parameter', 'float', 'sin({SystemStatus#my_parameter})'),
            )),
            Command('systemOn', (), lambda device, param, value, selector:
                                        device.set_state({"SystemStatus#status": 1}, selector)),
            Command('systemOff', (), lambda device, param, value, selector:
                                        device.set_state({"SystemStatus#status": 0}, selector)),
        )
        # Create the first device
        first_device = IntervalUpdateDevice(
                                                # List of fields that will be updated at 30 Hz, with its TimingSelector
                                                [("SystemStatus#my_parameter", TimingSelector("LHC.USER.ALL"))],
                                                # Name of the device to simulate
                                                "MY.AMZNG.TST.DEVC-000-DIBEV3",
                                                # The ones set above with Settings, Acquisitions and Commands
                                                first_device_properties,
                                                # Tuple containing a list of the TimingSelectors your app will use to get the data from this mocked device.
                                                timing_selectors=(TimingSelector(""), TimingSelector("LHC.USER.ALL")),
                                                # Update frequency
                                                frequency=30
                                            )
        # Start the device's timer
        device.time_tick()
        # Add the new device to your list
        my_list_of_devices.append(first_device)
        ...
        <define all your devices like done for the first>
        ...

        # Create the System and the simulated PyJapc
        my_system = System(devices=my_list_of_devices)
        mocked_pyjapc = SimulatedPyJapc.from_simulation_factory(lambda: my_system)

        # Monkey-patch PyJapc
        pyjapc.PyJapc = mocked_pyjapc


    if __name__ == "__main__":
        # Call the mocking function above
        setup_papc_simulation()

        # Start your app and verify that it's receiving your simulated data.
        app = QApplication(sys.argv)
        window = MyMainWindow()
        window.show()
        sys.exit(app.exec_())

To summarize:

 * You subclass the Device class in order to behave like your device/s. In the example, ``IntervalUpdateDevice``
   simulated a device that keeps increasing a field (``SystemStatus#my_parameter``) at the specified frequency
   (30 Hz). A basic ``Device``, instead, simply reacts to SET operations and to Commands.

 * For each device, you create a tuple (``device_properties``) which contains a list of ``Acquisition``, ``Setting``
   and/or ``Command`` properties, each ones with their respective fields (or ``Commands`` with their lambdas).
   Fields can be regular ``FieldTypes`` or ``EquationFieldTypes``, which take a third parameter that describes
   how the field changes with respect to another field in the same device (like ``SystemData#sin_of_my_parameter``)

 * For each device, you specify a list of the ``TimingSelectors`` your app will use to fetch the data.

 * You instantiate the device and add it to you list of devices.

 * You pass the list of devices you created to the constructor of ``System``

At this point, the application is sandboxed and should be able to start also on a machine that has no access to
the control system.

If you are using this setup for tests, remember to put all the setup code in a ``pytest``'s fixture, so that the simulation
environment is setup from scratch for every test. See the `testing page <7-testing.html>`_
for an example of how to properly do it.

.. index:: Troubleshooting ``papc``
.. _papc_troubleshooting:

Troubleshooting
===============

The tests seems to run fine on my machine, but hang on the CI
-------------------------------------------------------------
Make sure the monkey-patching process is really done for each test. Add ``autouse=True`` to the fixture's
decorator to make absolutely sure this is always done.

The tests seems to get slower and slower after the first 5-6 tests
------------------------------------------------------------------
First, make sure the last tests are slower even if you randomize the order of execution with ``--random-order``.
This flag might cause your tests to break if they are not isolated properly, i.e. they influence each other.
If your test cannot be run in random order, please review them and make them independent.

If the issue persists, it might be a ``papc`` problem.
``papc`` seems to have trouble being garbage collected at times. Add ``scope="session"`` to the fixture's decorator
to make ``pytest`` reuse the ``papc`` instance instead of creating new ones.
Pay strong attention to avoid side effects.



.. index:: papc FAQ
.. _papc_faq:

FAQ
===

*TODO*
