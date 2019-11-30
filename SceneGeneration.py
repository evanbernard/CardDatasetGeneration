from Constants import *
from BackgroundImages import Backgrounds
from CardImages import Cards
from CardExtractor import rotate_bound


#chang
class Scene:
    def __init__(self):
        self.bg_images = Backgrounds()
        self.card_images = Cards()

    def create_single_card(self):
        # TODO when rotating the labels make sure you check to see if they're off the image
        #   if the are, then dont include that image in the training data
        new_bg = self.bg_images.get_random()
        # Our backgrounds are a little small, so apply a random resize
        random_size = random.uniform(1, 3)
        new_bg = cv2.resize(new_bg, (int(new_bg.shape[1]*random_size), int(new_bg.shape[0]*random_size)))
        # We will be resizing multiple times so we need to save our starting width and height so we know what size
        #   it should be at the end
        old_width = new_bg.shape[0]
        old_height = new_bg.shape[1]

        new_card = self.card_images.get_random()

        angle = random.randint(0, 360)

        # Note: if we were to rotate the card first then put it on the background we would have had either a cropped
        #   card or a card with black corners, which is no good, so we took the approach of rotating the bg instead
        # We first rotate the background by a random angle, note that rotate_bound will resize the image to make sure
        #   that the image doesn't get cropped at all (ie, it is sized up so that the corners aren't cut off)
        new_bg = rotate_bound(new_bg, angle, [])
        # Now that we have our rotated background, we can place a card vertically on that background
        new_bg = place_card(new_card, new_bg)
        # Now we need to rotate the background back to the original position so we have effectively rotated the card
        #   on the background
        new_bg = rotate_bound(new_bg, -angle, [])

        # We are left with an image with black borders of size old_width/2 because of the resizing, so lets grab the
        #   middle of the image to crop the black off
        new_bg = new_bg[int((new_bg.shape[0] - old_width)/2):int((new_bg.shape[0] + old_width)/2),
                        int((new_bg.shape[1] - old_height)/2):int((new_bg.shape[1] + old_height)/2)]

        cv2.imshow("rotated card", new_bg)
        cv2.waitKey(0)

    def create_double_card(self):
        pass

    def create_triple_card(self):
        pass


def main():
    newScene = Scene()
    while True:
        newScene.create_single_card()


def place_card(img, bg):
    height = bg.shape[0]
    width = bg.shape[1]

    x_card = random.randint(0, width - img.shape[1])
    y_card = random.randint(0, height - img.shape[0])
    bg[y_card:y_card+img.shape[0], x_card:x_card+img.shape[1]] = img

    return bg


if __name__ == "__main__":
    main()
