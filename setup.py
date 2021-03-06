"""
setup.py for demo-.

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
        "accwidgets",
        "pyjapc",
        "papc",  # For sandbox mode and tests
    ],
    'test': [
        "pytest",
        "pytest-qt",
        "pytest-cov",
        "pytest-random-order",
    ],
    'dev': [
    ],
    'doc': [
        'sphinx',
        'acc-py-sphinx',
    ],
}


setup(
    name='demo',
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
            'run-example-1=demo.example_1_simple_form.main:main',
            'run-example-2=demo.example_2_image.main:main',
            'run-example-3=demo.example_3_plot.main:main',
        ],
    },
)
