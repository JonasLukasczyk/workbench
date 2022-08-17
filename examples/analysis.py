import cinemasci
import matplotlib
from PIL import Image
import numpy
import sys
import os.path
from os import mkdir
import argparse

#
# script to analyze a collection of cinema databases and
# store the results of that analysis
#
#------------------------------------------------------------

# Pulls a list of directories to analyze
parser = argparse.ArgumentParser()
parser.add_argument('--databases', 
                    help="list of directories to analyze", 
                    required=True,
                    nargs='+')
parser.add_argument("-o",'--output',
                    help="Name of the output file of your choice; somefile.csv", 
                    required=True)
                                   
args = parser.parse_args()
	
# use argparse to collect command line args
for d in args.databases:
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
    os.mkdir(os.path.join(d, "canny"))
    outpath = os.path.join(d, "canny", args.output)
    with open(outpath, 'w') as output:
        output.write("average pixel,num edge pixels\n")
        for image in imageCanny.outputs.Images.get():
            img = Image.fromarray(image.channel['Canny'], 'L')
            path = os.path.join( d, "canny", "canny_{:03}.png".format(curid) )
            white_pix = numpy.sum(image.channel['Canny'] == 1.0)
            img.save(path)
            curid += 1 

            output.write("{},{}\n".format(numpy.mean(image.channel['Canny']), white_pix))
