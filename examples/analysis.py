import cinemasci
import matplotlib
from PIL import Image
import numpy
import sys
import os.path

#
# script to analyze a collection of cinema databases and
# store the results of that analysis
#

#
# TODO 
#
# 1. replace the command line argument handling section
#    with code using argparse. 
#
#    Needed: arg that is a list of directories to operate on
#    example:
#        python analysis.py --somename sphere.cdb cinema.cdb
#

#
# handle command line arguments
#
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
