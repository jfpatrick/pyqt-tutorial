from typing import List
from papc.interfaces.pyjapc import SimulatedPyJapc
from papc.system import System
from papc.device import Device
from papc.fieldtype import FieldType, EquationFieldType
from papc.deviceproperty import Acquisition, Setting
from papc.timingselector import TimingSelector

from demo.papc_setup.papc_utils import IntervalUpdateDevice


def setup_papc_devices() -> SimulatedPyJapc:
    """
    This function sets up the JAPC simulation environment using papc.
    """
    # Creates the hierarchy of simulated objects (devices, properties, fields, selectors...)
    list_of_devices = create_my_devices()

    # Instantiates a papc System (interface for a group of devices)
    my_system = System(devices=list_of_devices)

    # Create a JAPC-like interface for the System above.
    # This interface can be used to monkeypatch (replace at runtime) a JAPC instance.
    return SimulatedPyJapc.from_simulation_factory(lambda: my_system, strict=False)


def create_my_devices() -> List[Device]:
    """
    This function describes in detail how to simulate a JAPC device
    and instantiates the hierarchy of objects required for the simulation.
    You can find more information regarding papc simulations
    on the Acc-Py wikis:
    https://wikis.cern.ch/display/ACCPY/papc+-+a+pure+Python+PyJapc+offline+simulator
    """
    # List the devices properties and fields and their relationships
    device_properties = (
        Setting('Settings', (
            FieldType("status", "int", initial_value=1),
            FieldType("name", "str", initial_value="My System"),
            FieldType("amplitude_sin", "int", initial_value=50),
            FieldType("amplitude_cos", "int", initial_value=50),
            FieldType("period_sin", "int", initial_value=50),
            FieldType("period_cos", "int", initial_value=50),
            FieldType("theta", "float", initial_value=0)
        )),
        Acquisition('Acquisition', (
            EquationFieldType('sin', 'float',
                              'sin({Settings#theta}/({Settings#period_sin}/30))*{Settings#amplitude_sin}'),
            EquationFieldType('cos', 'float',
                              'cos({Settings#theta}/({Settings#period_cos}/30))*{Settings#amplitude_cos}'),
        )),
        # Next PAPC release will enable these fields too
        # Command('systemOn', (), start_the_device),
        # Command('systemOff', (), stop_the_device),
    )
    # Instantiate a device using the above information - see IntervalUpdateDevice
    device = IntervalUpdateDevice(
                        name="TEST_DEVICE",
                        device_properties=device_properties,
                        field_to_update="Settings#theta",
                        selector_to_update=TimingSelector("LHC.USER.ALL"),
                        timing_selectors=(TimingSelector(""), TimingSelector("LHC.USER.ALL")),
                        frequency=30
                    )
    return [device]


def start_the_device(device, param, value, selector) -> None:
    """ Callback for the systemOn Command """
    device.set_state({"SystemStatus#status": 1}, selector)
    device.timer.resume()


def stop_the_device(device, param, value, selector) -> None:
    """ Callback for the systemOff Command """
    device.set_state({"SystemStatus#status": 0}, selector)
    device.timer.pause()
