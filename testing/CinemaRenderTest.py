import pytest
import pytest_xvfb

import os
import cinemasci

@pytest.fixture(autouse=True, scope='session')
def ensure_xvfb():
  if not pytest_xvfb.xvfb_available():
    raise Exception("Tests need Xvfb to run.")

def test_render():
  scratchdir = os.path.join( "testing", "scratch" )
  cdbpath    = os.path.join( scratchdir, "cinema.cdb" )

  try:
    os.makedirs(scratchdir)
  except OSError as error:
    pass

  # create a test database
  os.system("./cinema --database {}".format(cdbpath))
  assert os.path.isdir(scratchdir)
  assert os.path.isdir(cdbpath)

  # open a cinema database
  cdb = cinemasci.CinemaDatabaseReader();
  cdb.inputs.Path.set( cdbpath );

  # Select Some Data Products\n",
  query = cinemasci.DatabaseQuery();
  query.inputs.Table.set(cdb.outputs.Table);
  query.inputs.Query.set('SELECT * FROM input LIMIT 5 OFFSET 0');

  # Read Data Products
  imageReader = cinemasci.ImageReader();
  imageReader.inputs.Table.set(query.outputs.Table)

  # Render Data Products
  imageRenderer = cinemasci.ImageRenderer();
  imageRenderer.inputs.Images.set( imageReader.outputs.Images );

  # print images
  images = imageRenderer.outputs.Images.get();
  print(images)
