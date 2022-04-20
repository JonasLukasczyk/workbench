import pytest
import pytest_xvfb

import os
import cinemasci

@pytest.fixture(autouse=True, scope='session')
def ensure_xvfb():
  if not pytest_xvfb.xvfb_available():
    raise Exception("Tests need Xvfb to run.")

def test_render():
   # create a test database
  os.system("./bin/create-database --database scratch/cinema.cdb")

  # open a cinema database
  cdb = cinemasci.DatabaseReader();
  cdb.inputs["Path"].setValue( 'scratch/cinema.cdb' );

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
