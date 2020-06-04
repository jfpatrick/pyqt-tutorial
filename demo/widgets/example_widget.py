import logging

from PyQt5.QtWidgets import QTabWidget, QSpinBox
from accwidgets.graph import TimeSpan, ScrollingPlotWidget

# Import the models
from demo.models.data_source import ExampleModel, DeviceTimingSource, SinglePointSource

# Import the code generated from the example_widget.ui file
from demo.resources.generated.ui_example_widget import Ui_TabWidget


class ExampleWidget(QTabWidget, Ui_TabWidget):
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
        super(ExampleWidget, self).__init__(parent)

        # Instantiate the view
        self.setupUi(self)

        # Instantiate the model
        self.model = ExampleModel()

        # Setup the plots
        scrolling_plot = self.findChild(ScrollingPlotWidget, "scrolling_plot")
        self._setup_plot(scrolling_plot, parameter="BISWRef1/Acquisition#angle", selector="")

        # Setup the control widgets for amplitude and period:
        # - Select the widget
        frequency_scrolling_plot = self.findChild(QSpinBox, "frequency_scrolling_plot")
        # - Set their initial value reading it from the devices
        frequency_scrolling_plot.setValue(self.model.get_frequency())
        # - Connect them to the device to be able to set
        frequency_scrolling_plot.valueChanged.connect(self.model.set_frequency)

        # Log something to see it in the LogDisplay Widget
        logging.debug("This message won't be visible, because the default log level is INFO")
        logging.info("This is a message from the application.")

    def _setup_plot(self, plot_widget, parameter, selector):
        # Create the data sources - timing and data
        timing_source = DeviceTimingSource(parameter, selector)
        data_source = SinglePointSource(parameter, selector)

        # Connect plot and data source
        plot_widget.timing_source = timing_source
        plot_widget.addCurve(data_source=data_source)

        # Setup the plot
        plot_widget.time_span = TimeSpan(10.0, 0.0),
        plot_widget.time_progress_line = True
