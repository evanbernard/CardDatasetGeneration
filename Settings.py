# The image size is divided by reduce when displayed
REDUCE = 5

# CardExtractor.py SETTINGS---------------------------------------------------------------------------------------------

# cardName has the format {suit}{value}, where a 10 has a value of 0 and ace has a value of A
# If ALL_CARDS is false, CardExtractor will run only on this card
CARD_NAME = "S0"
# some predefined settings, when testing_extract, it will show everything but not export the files, when export_extract,
#   it will only export the files
TESTING_EXTRACT = False
EXPORT_EXTRACT = False
# The final image size of the cropped images
IM_SIZE = (300, 420)
# Display the cropped card after CardExtractor.py is run
SHOW_IM = True
SHOW_CONTOURS = False
# Show the threshold, original image, rotated image and final image in CardExtractor
SHOW_DETAILS = False
# If EXPORT is true, the cropped image will be saved to the specified folder
EXPORT = False
# Run CardExtractor over all cards in folder
ALL_CARDS = True
# Have the CardExtractor cropped image horizontal (height less than width)
HORIZONTAL = False
