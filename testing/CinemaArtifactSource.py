import unittest
import cinemasci
import os
from matplotlib.testing.compare import compare_images

class CinemaArtifactSourceTest(unittest.TestCase):
    gold    = "testing/gold"
    scratch = "testing/scratch"

    def __init__(self, *args, **kwargs):
        super(CinemaArtifactSourceTest, self).__init__(*args, **kwargs)

    def setUp(self):
        try:
            os.makedirs(os.path.join(CinemaArtifactSourceTest.scratch, "artifact"))
        except OSError as error:
            pass

        print("Running test: {}".format(self._testMethodName))

    def compare(self, a, b ): 
        # '25' is a tolerance value, to be replaced when images can be inspected
        results = compare_images( a, b, 25 )

        return (results is None)

    def test_artifact_source(self):
        # create an artifact source
        artifactSource = cinemasci.TestImageArtifactSource();

        # provide input parameters and save the resulting images
        artifactSource.inputs["Parameters"].setValue( {'phi': 25.5, 'theta': 50.0} );
        images = artifactSource.outputs["Artifacts"].getValue();
        for i in images:
            i.save(os.path.join(CinemaArtifactSourceTest.scratch, "artifact", "imagesource.png"))

        # check the results
        gold = os.path.join(CinemaArtifactSourceTest.gold, "artifact", "imagesource.png" ) 
        scratch = os.path.join(CinemaArtifactSourceTest.scratch, "artifact", "imagesource.png" )
        self.assertTrue(os.path.exists(scratch))
        result = self.compare( gold, scratch ) 
        self.assertTrue(result)

    def test_cinema_artifact_source(self):
        # create an artifact source
        artifactSource = cinemasci.CinemaArtifactSource()
        # point it to a database
        artifactSource.path = os.path.join(CinemaArtifactSourceTest.gold, "artifact", "cinema.cdb") 
        artifactSource.inputs["Parameters"].setValue( {'phi': 10.0, 'theta': 110.0} );
