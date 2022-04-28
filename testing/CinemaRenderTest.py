import pytest
import pytest_xvfb

import os
import cinemasci

@pytest.fixture(autouse=True, scope='session')
def ensure_xvfb():
  if not pytest_xvfb.xvfb_available():
    raise Exception("Tests need Xvfb to run.")

def test_render():
  scratchdir = "testing/scratch"
  # make the test area
  try:
    os.makedirs(scratchdir)
  except OSError as error:
    pass

  print(scratchdir)
  assert os.path.isdir(scratchdir)

  # create a test database
  os.system("cinema --database testing/scratch/cinema.cdb")

  # open a cinema database
  cdb = cinemasci.CinemaDatabaseReader();
  cdb.inputs["Path"].setValue( 'testing/scratch/cinema.cdb' );

  # Select Some Data Products\n",
  query = cinemasci.DatabaseQuery();
  query.inputs["Table"].setValue(cdb.outputs['Table']);
  query.inputs["Query"].setValue('SELECT * FROM input LIMIT 5 OFFSET 0');

  # Read Data Products
  imageReader = cinemasci.ImageReader();
  imageReader.inputs["Table"].setValue(query.outputs['Table'])

  # Read Data Products
  imageRenderer = cinemasci.ImageRenderer();
  imageRenderer.inputs["Image"].setValue( imageReader.outputs["Images"] );

  # print images
  images = imageRenderer.outputs["Image"].getValue();
  print(images)
