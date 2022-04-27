import unittest
import cinemasci

class CinemaArtifactSourceTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(CinemaArtifactSourceTest, self).__init__(*args, **kwargs)

    def setUp(self):
        print("Running test: {}".format(self._testMethodName))

    def test_artifact_source(self):
        artifactSource = cinemasci.TestImageArtifactSource();
        artifactSource.inputs["Parameters"].setValue( {'phi': 25.5, 'theta': 50.0} );
        images = artifactSource.outputs["Artifacts"].getValue();
        for i in images:
            i.save("test.png")
