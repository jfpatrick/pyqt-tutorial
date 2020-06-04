
# Generate the code from .ui and .qrc files in case they are missing or outdated
import os
import pyqt5ac
pyqt5ac.main(config=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pyqt5ac.yml'))