import cinemasci
import matplotlib
from PIL import Image
import numpy
import sys
import os.path

databases = []
if len(sys.argv) == 1:
    print("ERROR: Need a list of directories to work on")
    exit()

else:
    databases = sys.argv[1:] 

# use argparse to collect command line args
for d in databases:
    # Open Cinema Database
    cdb  = cinemasci.CinemaDatabaseReader();
    cdb.inputs.Path.set( d ); 

    # Select Some Data Products
    query = cinemasci.DatabaseQuery();
    query.inputs.Table.set(cdb.outputs.Table);
    query.inputs.Query.set('SELECT * FROM input');

    # Read Data Products
    imageReader = cinemasci.ImageReader();
    imageReader.inputs.Table.set(query.outputs.Table);

    # Render in black and white# Run an algorithm on the images
    imageConvert = cinemasci.ImageConvert();
    imageConvert.inputs.Conversion.set( cinemasci.ImageConvertType.COLOR );
    imageConvert.inputs.Images.set( imageReader.outputs.Images );

    # Run canny algorithm
    imageCanny = cinemasci.ImageCanny();
    # imageCanny.inputs.Thresholds.set( [0, 70] )
    imageCanny.inputs.Images.set( imageConvert.outputs.Images );

    # Display Results
    from IPython.display import display
    curid = 0
    for image in imageCanny.outputs.Images.get():
        img = Image.fromarray(image.channel['Canny'], 'L')
        path = os.path.join( d, "canny_{:03}.png".format(curid) )
        print(path)
        img.save(path)
        curid += 1
