import sys
import os

# Ensure the src directory is in the Python path
print ("Python path: ", os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from .tests_base import *
from .tests_quandela import *
from .tests_photonic_indistinguishability import *
from .tests_tomography import *
