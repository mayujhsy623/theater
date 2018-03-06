import os
from setuptools import setup

requirements = open(
    os.path.join(os.path.dirname(__file__),
                 'requirements.txt')).readlines()

setup(
    name='theater',
    version='0.1',
    description='virtual seller',
    packages=['theater'],
    install_requires=requirements,
)