from Constants import *


# The Cards class is a class containing all the cropped cards we have in a pickle file
# This class is used for grabbing (a) random card(s) and combining it with random background image
class Cards:
    def __init__(self):
        self.images = pickle.load(open(cardPickleLoc, 'rb'))
        self.nb_images = len(self.images)
        # print("Number of cards loaded :", self.nb_images)

    def get_random(self, display=False):
        card = self.images[random.randint(0, self.nb_images - 1)]
        if display:
            cv2.imshow("Random Card", card)
            cv2.waitKey(0)
        return card


# create_pickle() creates a pickle file of all of the cards found in
#   the file location cardLocation (found in Constants.py)
def create_pickle():
    save_name = "cardPickle"
    # All images will be temporarily stored in card_images
    card_images = []
    # We just need to parse through each
    for f in glob(cardLocation+"/*.jpg"):
        card_images.append(mpimg.imread(f))
    print("Number of images loaded :", len(card_images))
    print("Saved in :", save_name)
    pickle.dump(card_images, open(save_name, 'wb'))


if __name__ == "__main__":
    # create_pickle()
    cards = Cards()
    while True:
        cards.get_random(display=True)
