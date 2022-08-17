import cinemasci
import matplotlib
from PIL import Image
import numpy
import sys
import os.path
import argparse
import cv2 as cv
#
# script to analyze a collection of cinema databases and
# store the results of that analysis
#

#
# TODO 
#
# 1. add a command line argument called 'output' that lets 
#    the user define a name for an output file for analysis 
#    data, with the default value being 'analysis.csv'
#    This file will contain a line for each input image,
#    which contains values we compute
#
#    Using the new command when you are done should look
#    something like this:
#    
#      python3 analysis.py --dataases cinema.cdb sphere.cdb --output somefile.csv
#
# 2. For each database given in the directory list (in
#    the 'directory' command line argument):
#    a. create a file that is named what the 'file' command
#       line argument is
#    b. for each of the images you read in for that database
#       1. compute the average pixel of the image (r,g,b)
#       2. compute the number of white pixels in the canny image
#       3. compute the probability of a pixel being white
#          in the canny image
#       4. write out a line in the file that is three values,
#          each separated by a comma:
#          a. average pixel value (r,g,b0
#          b. num white pixels 
#          c. probability that a pixel is an edge pixel 
#          Each line should look like something like this:
#             "124,34,145",234,0.9
#
# You will have to use the 'format' command to create the 
# string to write into the file,
#
# Look at this link for an example of opening and closing a 
# new text file:
#     https://www.pythontutorial.net/python-basics/python-create-text-file/
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
                    required=True,
                    nargs='+')
                                   
args = parser.parse_args()
for d in args.databases:
	print (d)
	
	#----------------------------------------------------------------------------------------------------------------------------------


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
    for image in imageCanny.outputs.Images.get():
        img = Image.fromarray(image.channel['Canny'], 'L')
        path = os.path.join( d, "canny_{:03}.png".format(curid) )
        white_pix = numpy.sum(img == 255)
        black_pix = numpy.sum(img == 0)
        #with open('analysis.txt', 'w') as output:
        	#output.write(print("Average Pixel Value:", numpy.mean(img.size), ", Num white pixels: ", white_pix,", Num black pixels: ", black_pix, )
        #print(img.size)
        #print(numpy.mean(img.size))
        print(path)
        img.save(path)
        curid += 1 
with open('analysis.txt', 'w') as output:
        	output.write(print("Average Pixel Value:{}, Num white pixels:{}  Num black pixels:{} ".format('numpy.mean(img.size)', 'white_pix', 'black_pix')))
