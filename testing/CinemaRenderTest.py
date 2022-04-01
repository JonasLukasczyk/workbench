import unittest
import os
import cinemasci

class CinemaRenderTest(unittest.TestCase):
    gold    = "testing/gold"
    scratch = "testing/scratch"

    def __init__(self, *args, **kwargs):
        super(CinemaRenderTest, self).__init__(*args, **kwargs)

    def setUp(self):
        print("Running test: {}".format(self._testMethodName))

    def test_smoketest(self):
        # Render Images in Black and White (to demo shader effects)
        imageRenderer = cinemasci.ImageRenderer()
        imageRenderer.smoke_test()

