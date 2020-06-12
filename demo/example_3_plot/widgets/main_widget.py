from typing import Callable
import logging

from PyQt5.QtWidgets import QWidget, QSpinBox
from accwidgets.graph import TimeSpan, ScrollingPlotWidget

# Import the models
from demo.example_3_plot.models.models import JapcModel, DeviceTimingSource, SinglePointSource

# Import the code generated from the view.ui file
from demo.example_3_plot.resources.generated.ui_view import Ui_Form


class MainWidget(QWidget, Ui_Form):
    """
        This is the main class defining your GUI. In an MVP perspective,
        this is a Presenter, so a component acting as a proxy between Model
        and View.

        The Model will connect to the control systems or any other source of data.
        The View is the code generated from your *.ui files.

        Signals and slots are usually connected in this class, in the init.
        The model will usually emit signal which are catch either directly
        by the View, or by this class, which translates them into operations
        on the View.

        In this example we are connecting the plots on the View with the DataSources
        classes defined in the model, and the SpinBoxes below the plots with the custom
        ExampleModel class, that performs PyJAPC SET operations.
    """
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        # Instantiate the view
        self.setupUi(self)

        # Instantiate the model
        self.model = JapcModel()

        # Setup the plots
        scrolling_plot = self.findChild(ScrollingPlotWidget, "scrolling_plot")
        self._setup_plot(plot_widget=scrolling_plot, parameter="TEST_DEVICE/Acquisition#sin", selector="LHC.USER.ALL")

        # Setup the spinbox widgets
        self._setup_spinbox(spinbox_name="amplitude_sin",
                            initial_value=self.model.get_amplitude_sin(),
                            connect_to=self.model.set_amplitude_sin)
        self._setup_spinbox(spinbox_name="period_sin",
                            initial_value=self.model.get_period_sin(),
                            connect_to=self.model.set_period_sin)

        # Log something to see it in the LogDisplay Widget
        logging.debug("This message won't be visible, because the default log level is INFO")
        logging.info("This is a message from the application.")

    def _setup_plot(self, plot_widget: 'PlotWidget', parameter: str, selector: str) -> None:
        """
        Sets up the plots by connecting the widgets on the View to their relative Models.
        :param plot_widget: the widget selected from the View
        :param parameter: The JAPC parameter to take data from
        :param selector: The JAPC selector to use
        :return: None
        """
        # Create timing source
        timing_source = DeviceTimingSource(parameter, selector)
        # Connect the timing source to the plot
        plot_widget.timing_source = timing_source

        # Create the data source
        data_source = SinglePointSource(parameter, selector)
        # Add the data source as a curve in the plot
        plot_widget.addCurve(data_source=data_source)

        # Setup other plot properties
        plot_widget.time_span = TimeSpan(10.0, 0.0),
        plot_widget.time_progress_line = True

    def _setup_spinbox(self, spinbox_name: str, initial_value: int, connect_to: Callable) -> None:
        """
        Sets up the spinbox by setting their initial values and then connecting them to the JAPC SET function
        exposed by the ``ExampleModel`` class.
        :param spinbox_name: The name of the Spinbox widget on the View
        :param initial_value: The initial value to display on the widget
        :param connect_to: the function that performs the SET when a new value is entered in the spinbox.
        :return: None
        """
        # Find the SpinBox by name in the View
        spinbox = self.findChild(QSpinBox, spinbox_name)
        # Set its initial value
        spinbox.setValue(initial_value)
        # Connect it to the control system to make it able to SET
        spinbox.valueChanged.connect(connect_to)