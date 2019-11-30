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

cardLocation = "Z:\\ML_Images\\Playing_Cards\\Images\\"
cardPickleLoc = "Z:\\ML_Images\\Playing_Cards\\cardPickle"

# cardName has the format {suit}{value}, where a 10 has a value of 0 and ace has a value of A
cardName = "H2"
# The image size is divided by reduce when displayed
REDUCE = 5
SHOW_CONTOURS = False
# Show the threshold, original image, rotated image and final image
SHOW_DETAILS = True
# If export is true, the final image will be saved to the specified folder
EXPORT = False
# Run the script over all cards in folder
ALL_CARDS = False
# Have the final image horizontal (height less than width)
HORIZONTAL = False
