import imutils
import cv2
import numpy as np
import os
import math
import pickle
from glob import glob
import random

imFolder = "Cards"
imExtension = ".jpg"
cardFolder = "CroppedCards"

bgLocation = "Z:\\ML_Images\\Background_Dataset\\Images\\"
bgPickleLoc = "Z:\\ML_Images\\Background_Dataset\\BGPickle"

cardLocation = "CroppedCards\\" #"Z:\\ML_Images\\Playing_Cards\\Images\\"
cardPickleLoc = "Z:\\ML_Images\\Playing_Cards\\cardPickle"

# some predefined settings, when testing_extract, it will show everything but not export the files, when export_extract,
#   it will only export the files
TESTING_EXTRACT = False
EXPORT_EXTRACT = False

# cardName has the format {suit}{value}, where a 10 has a value of 0 and ace has a value of A
cardName = "SA"

# The image size is divided by reduce when displayed
REDUCE = 5

# The final image size of the cropped images
IM_SIZE = (300, 420)

# Display the cropped card after CardExtractor.py is run
SHOW_IM = True
SHOW_CONTOURS = False
# Show the threshold, original image, rotated image and final image
SHOW_DETAILS = False
# If export is true, the final image will be saved to the specified folder
EXPORT = False
# Run the script over all cards in folder
ALL_CARDS = True
# Have the final image horizontal (height less than width)
HORIZONTAL = False
