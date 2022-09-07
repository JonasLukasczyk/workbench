import pytest
import pycinema
import os
from matplotlib.testing.compare import compare_images

gold        = "testing/gold"
scratch     = "testing/scratch"
do_setup    = True

def setUp():
    global do_setup
    global scratch

    if do_setup:
        try:
            os.makedirs(os.path.join(scratch, "artifact"))
            do_setup = False
        except OSError as error:
            pass


def compare( a, b ):
    # '25' is a tolerance value, to be replaced when images can be inspected
    results = compare_images( a, b, 25 )

    return (results is None)

def test_artifact_source():
    global scratch
    global gold

    setUp()

    # create an artifact source
    artifactSource = pycinema.TestImageArtifactSource();

    # provide input parameters and save the resulting images
    artifactSource.inputs.Parameters.set( {'phi': 25.5, 'theta': 50.0} );
    images = artifactSource.outputs.Artifacts.get();
    for i in images:
        i.save(os.path.join(scratch, "artifact", "imagesource.png"))

    # check the results
    resdir = os.path.join(gold, "artifact", "imagesource.png" )
    scratch = os.path.join(scratch, "artifact", "imagesource.png" )
    assert os.path.exists(scratch)
    result = compare( resdir, scratch )
    assert result

def test_cinema_artifact_source():
    global gold

    setUp()

    # create an artifact source
    artifactSource = pycinema.CinemaArtifactSource()
    # point it to a database
    artifactSource.path = os.path.join(gold, "artifact", "cinema.cdb")
    artifactSource.inputs.Parameters.set( {'phi': 10.0, 'theta': 110.0} );
