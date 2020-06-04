"""
setup.py for pyqt-mega-tutorial-for-be-bi.

For reference see
https://packaging.python.org/guides/distributing-packages-using-setuptools/

"""
from pathlib import Path
from setuptools import setup, find_packages


HERE = Path(__file__).parent.absolute()
with (HERE / 'README.md').open('rt') as fh:
    LONG_DESCRIPTION = fh.read().strip()


REQUIREMENTS: dict = {
    'core': [
        "pyqt5",
        "pyqt5ac @ git+https://:@gitlab.cern.ch:8443/szanzott/pyqt5ac.git",  # To automate the compilation of .ui and .qrc files
        "pyqtgraph",
        "be-bi-application-frame",
        "comrad",  # FIXME Provides the CLogDisplay, remove in favor of the real AppFrame or accwidgets'version when out
        "accwidgets",  # For the plots
        "pyjapc",  # FIXME Has to go after comrad to pick the right version?
    ],
    'test': [
        "pytest",
        "pytest-qt",
        "pytest-cov",
        "pytest-random-order",
        "papc",  # For the sandbox mode
    ],
    'dev': [
    ],
    'doc': [
        'sphinx',
        'acc-py-sphinx',
    ],
}


setup(
    name='pyqt-mega-tutorial-for-be-bi',
    version="0.0.1.dev0",

    author='Sara Zanzottera',
    author_email='sara.zanzottera@cern.ch',
    description='SHORT DESCRIPTION OF PROJECT',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='',

    packages=find_packages(),
    python_requires='>=3.6, <4',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIREMENTS['core'],
    include_package_data=True,
    extras_require={
        **REQUIREMENTS,
        # The 'dev' extra is the union of 'test' and 'doc', with an option
        # to have explicit development dependencies listed.
        'dev': [req
                for extra in ['dev', 'test', 'doc']
                for req in REQUIREMENTS.get(extra, [])],
        # The 'all' extra is the union of all requirements.
        'all': [req for reqs in REQUIREMENTS.values() for req in reqs],
    },
    entry_points={
        'console_scripts': [
            'run-demo=demo.main:main',
        ],
    },
)
