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
        # create a test database
        os.system("./bin/create-database --database scratch/cinema.cdb")

        # open a cinema database
        cdb  = cinemasci.DatabaseReader();
        cdb.inputs["Path"].setValue( 'scratch/cinema.cdb' );

        # Select Some Data Products\n",
        query = cinemasci.DatabaseQuery();
        query.inputs["Table"].setValue(cdb.outputs['Table']);
        query.inputs["Query"].setValue('SELECT * FROM input LIMIT 5 OFFSET 0');

        # Read Data Products
        imageReader = cinemasci.ImageReader();
        imageReader.inputs["Table"].setValue(query.outputs['Table'])

