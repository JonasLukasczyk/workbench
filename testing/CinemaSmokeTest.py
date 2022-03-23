import unittest

class CinemaSmokeTest(unittest.TestCase):
    gold    = "testing/gold"
    scratch = "testing/scratch"

    def __init__(self, *args, **kwargs):
        super(CinemaSmokeTest, self).__init__(*args, **kwargs)

    def setUp(self):
        print("Running test: {}".format(self._testMethodName))

    def test_smoketest(self):
        print("Cinema smoke test")
