from Constants import *


# The Backgrounds class is a class containing all the backgrounds we have in a pickle file
# This class is used for grabbing a random background and combining it with (a) random card(s)
class Backgrounds:
    def __init__(self):
        self.images = pickle.load(open(bgPickleLoc, 'rb'))
        self.nb_images = len(self.images)
        # print("Number of backgrounds loaded :", self.nb_images)

    # get_random will return the random background found in the bg pickle and display it if True is passed
    def get_random(self, display=False):
        bg = self.images[random.randint(0, self.nb_images - 1)]
        if display:
            cv2.imshow("Random Background", bg)
            cv2.waitKey(0)
        return bg



# create_pickle() creates a pickle file of all of the background images found in
#   the file location bgLocation (found in Constants.py)
def create_pickle():
    save_name = "BGPickle"
    # All images will be temporarily stored in bg_images
    bg_images = []
    # The folder is full of folders classifying the images,
    #   so we need to search each sub-folder of bgLocation and
    #   grab all the .jpgs
    for subdir in glob(bgLocation+"/*"):
        for f in glob(subdir+"/*.jpg"):
            bg_images.append(mpimg.imread(f))
    print("Number of images loaded :", len(bg_images))
    print("Saved in :", save_name)
    pickle.dump(bg_images, open(save_name, 'wb'))


if __name__ == "__main__":
    # create_pickle()
    backgrounds = Backgrounds()
    while True:
        backgrounds.get_random(display=True)
