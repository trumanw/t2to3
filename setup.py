"""
t2to3
A command-line interface to run the python 2to3 on a Python project.
"""
import sys
from setuptools import setup, find_packages
import versioneer

short_description = __doc__.split("\n")

# from https://github.com/pytest-dev/pytest-runner#conditional-requirement
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

try:
    with open("README.md", "r") as handle:
        long_description = handle.read()
except:
    long_description = short_description

setup(
    name='t2to3',
    author='XtalPi',
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license='MIT License',
    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        'Click',
        'tqdm',
    ],

    tests_require=[
        'pytest',
        'pytest-cov',
        'Click',
        'tqdm',
    ],

    setup_requires=[] + pytest_runner,
    entry_points={
        'console_scripts': ['t2to3=t2to3.cmd.cmd:main']
    }
)