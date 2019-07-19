from .models import Contract,Custom
import unittest

# Create your tests here.
class test(unittest.TestCase):
    def tests(self):
        print(Contract.__class__,Contract.__class__.__name__)

unittest.main()

