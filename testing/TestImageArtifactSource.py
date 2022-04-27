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
        results = compare_images( a, b, 1 )

        return (results is None)

    def test_artifact_source(self):
        artifactSource = cinemasci.TestImageArtifactSource();
        artifactSource.inputs["Parameters"].setValue( {'phi': 25.5, 'theta': 50.0} );
        images = artifactSource.outputs["Artifacts"].getValue();
        for i in images:
            i.save(os.path.join(CinemaArtifactSourceTest.scratch, "artifact", "imagesource.png"))

        # check the result
        result = self.compare(  os.path.join(CinemaArtifactSourceTest.gold, "artifact", "imagesource.png" ), 
                                os.path.join(CinemaArtifactSourceTest.scratch, "artifact", "imagesource.png" ) )
        self.assertTrue(result)
