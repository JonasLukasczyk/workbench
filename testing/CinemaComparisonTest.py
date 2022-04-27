import unittest
import numpy
import os
import matplotlib.pyplot as plt
from matplotlib.testing.compare import compare_images

class CinemaComparisonTest(unittest.TestCase):
    gold    = "testing/gold"
    scratch = "testing/scratch"

    def __init__(self, *args, **kwargs):
        super(CinemaComparisonTest, self).__init__(*args, **kwargs)

    def setUp(self):
        try:
            os.makedirs(CinemaComparisonTest.scratch)
        except OSError as error:
            pass
        print("Running test: {}".format(self._testMethodName))

    def compare(self, a, b ): 
        results = compare_images( a, b, 1 )

        return (results is None)

    def test_cinema_image_compare(self):
        result = self.compare( os.path.join(CinemaComparisonTest.gold, "comparison", "000.png" ), os.path.join(CinemaComparisonTest.gold, "comparison", "000.png" ) )
        self.assertTrue(result)
