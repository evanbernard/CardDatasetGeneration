import imutils
import cv2
import numpy as np
import os
import math
import pickle
from glob import glob
import random

imFolder = "Images/"
imExtension = ".jpg"
cardFolder = "CroppedImages/"

bgLocation = "Z:\\ML_Images\\Background_Dataset\\Images\\"
bgPickleLoc = "Z:\\ML_Images\\Background_Dataset\\BGPickle"
cardPickleLoc = "Z:\\ML_Images\\Playing_Cards\\cardPickle"
