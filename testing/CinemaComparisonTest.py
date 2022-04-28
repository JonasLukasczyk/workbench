import pytest
import os
from matplotlib.testing.compare import compare_images

gold    = "testing/gold"
scratch = "testing/scratch"

def compare( a, b ): 
    results = compare_images( a, b, 1 )

    return (results is None)

def test_cinema_image_compare():
    try:
        os.makedirs(scratch)
    except OSError as error:
        pass

    assert compare( os.path.join(gold, "comparison", "000.png" ), os.path.join(gold, "comparison", "000.png" ) )
