import unittest
import numpy
import os
import matplotlib.pyplot as plt
from matplotlib.testing.compare import compare_images

class CinemaBaseTest(unittest.TestCase):
    gold    = "testing/gold"
    scratch = "testing/scratch"

    def __init__(self, *args, **kwargs):
        super(CinemaBaseTest, self).__init__(*args, **kwargs)

    def setUp(self):
        try:
            os.makedirs(CinemaBaseTest.scratch)
        except OSError as error:
            pass
        print("Running test: {}".format(self._testMethodName))

    def compare_to_gold_image(self, image, image_name):
        # test the image
        newimg_path = os.path.join(TextCBDGenerator.scratch_dir, image_name)
        goldimg_path = os.path.join(TextCBDGenerator.gold_dir, image_name)
        plt.axis('off')
        plt.imsave(newimg_path, image)

        results = compare_images( goldimg_path, newimg_path, 1)

        return (results is None)

    def test_cinema_image_compare(self):
        result = self.compare_to_gold_image( os.path.join(CinemaBaseTest.gold, "base", "000.jpg" ), os.path.join(CinemaBaseTest.gold, "base", "000.jpg" ) )
        self.assertFalse(result)
