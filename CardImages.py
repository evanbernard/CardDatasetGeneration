from Constants import *


# The Cards class is a class containing the dictionary of card names and cropped images we have in a pickle file
# This class is used for grabbing (a) random card(s) and combining it with random background image
class Cards:
    def __init__(self):
        self.images = pickle.load(open(cardPickleLoc, 'rb'))
        self.nb_images = len(self.images)

    def get_random(self, display=False):
        card_name = random.choice(list(self.images.keys()))
        card = self.images[card_name]
        if display:
            cv2.imshow("Random Card", card)
            cv2.waitKey(0)
        return card, card_name


# create_pickle() creates a pickle file of a dictionary with keys being the card name {SUIT}{VALUE} and the value is
#   the card image
def create_pickle():
    cards_dict = {}
    # save_name = "cardPickle"
    # All images will be temporarily stored in card_images
    # We just need to parse through each
    for f in glob(cardLocation+"/*.jpg"):
        # Extract from the file location+name only the file name
        card_name = f[len(cardLocation):len(f)-len(imExtension)]
        # Save the name of the card as a key with the value of the image
        cards_dict[card_name] = cv2.imread(f)
    print("Number of images loaded :", len(cards_dict))
    print("Saved in :", cardPickleLoc)
    pickle.dump(cards_dict, open(cardPickleLoc, 'wb'))


if __name__ == "__main__":
    create_pickle()
    cards = Cards()
    # while True:
    #    cards.get_random(display=True)
