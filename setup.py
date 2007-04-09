#!/usr/bin/env python

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

# Note to self:
# python setup.py sdist --formats=zip
# To create the zip file

# python setup.py --command-packages=setuptools.command bdist_egg
# To create the egg file

# python setup.py register
# to register with PyPI
# 

# create an egg and upload it
# setup.py register bdist_egg upload

# Set this on command line
# DISTUTILS_DEBUG=true
# 
setup(
    name='monitor-output',
    version='0.1.0',
    description="Monitor the output of program and cause events to happen.",
    long_description=
"""Run this program as a shell to your other program and have it monitor certain strings like "ERROR" or "WARNING".
When one of these events occurs you can have it turn the text bold (using ANSI terminal coloring) or put a message on the screen.

""",
    author='Scott Kirkwood',
    author_email='scottakirkwood@gmail.com',
    url='http://code.google.com/p/monitor-output/',
    download_url='http://monitor-output.googlecode.com/files/monitor-output-0.1.0.zip',
    keywords=['utility', 'Python', 'linux'],
    license='GNU GPL',
    platforms=['POSIX'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ], 
    packages=['monitoroutput', 'monitoroutput/plugins'],
    scripts=['scripts/monitor-output'],
    zip_safe=False,
)

