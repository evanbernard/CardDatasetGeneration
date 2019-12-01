from Constants import *
from BackgroundImages import Backgrounds
from CardImages import Cards
from CardExtractor import rotate_bound


class Scene:
    def __init__(self):
        self.bg_images = Backgrounds()
        self.card_images = Cards()

    def create_single_card(self):
        # TODO when rotating the labels make sure you check to see if they're off the image
        #   if the are, then dont include that image in the training data
        new_bg = self.bg_images.get_random()

        # Our backgrounds are a little small, so apply a random resize
        random_size = random.uniform(1, 2)
        new_bg = cv2.resize(new_bg, (int(new_bg.shape[1]*random_size), int(new_bg.shape[0]*random_size)))
        # We will be resizing multiple times so we need to save our starting width and height so we know what size
        #   it should be at the end
        old_width = new_bg.shape[0]
        old_height = new_bg.shape[1]

        card, card_name = self.card_images.get_random()
        angle = random.randint(0, 360)

        # Note: if we were to rotate the card first then put it on the background we would have had either a cropped
        #   card or a card with black corners, which is no good, so we took the approach of rotating the bg instead
        # We first rotate the background by a random angle, note that rotate_bound will resize the image to make sure
        #   that the image doesn't get cropped at all (ie, it is sized up so that the corners aren't cut off)
        new_bg = rotate_bound(new_bg, angle, [])
        # Now that we have our rotated background, we can place a card vertically on that background
        new_bg, _ = place_card(card, new_bg, None)

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
        new_bg = self.bg_images.get_random()
        # cv2.imshow("orig", new_bg)
        # Our backgrounds are a little small, so apply a random resize
        random_size = random.uniform(1, 2)
        new_bg = cv2.resize(new_bg, (int(new_bg.shape[1] * random_size), int(new_bg.shape[0] * random_size)))
        # We will be resizing multiple times so we need to save our starting width and height so we know what size
        #   it should be at the end
        old_width = new_bg.shape[0]
        old_height = new_bg.shape[1]

        card1, card1_name = self.card_images.get_random()
        card2, card2_name = self.card_images.get_random()
        angle = random.randint(0, 360)

        # Note: if we were to rotate the card first then put it on the background we would have had either a cropped
        #   card or a card with black corners, which is no good, so we took the approach of rotating the bg instead
        # We first rotate the background by a random angle, note that rotate_bound will resize the image to make sure
        #   that the image doesn't get cropped at all (ie, it is sized up so that the corners aren't cut off)
        new_bg = rotate_bound(new_bg, angle, [])
        # Now that we have our rotated background, we can place a card vertically on that background
        new_bg, cords = place_card(card1, new_bg, None)
        small_angle = random.randint(-15, 15)
        new_bg = rotate_bound(new_bg, small_angle, [])
        new_bg, _ = place_card(card2, new_bg, cords)
        # Now we need to rotate the background back to the original position so we have effectively rotated the card
        #   on the background
        new_bg = rotate_bound(new_bg, -(angle + small_angle), [])

        # We are left with an image with black borders of size old_width/2 because of the resizing, so lets grab the
        #   middle of the image to crop the black off
        new_bg = new_bg[int((new_bg.shape[0] - old_width) / 2):int((new_bg.shape[0] + old_width) / 2),
                        int((new_bg.shape[1] - old_height) / 2):int((new_bg.shape[1] + old_height) / 2)]

        cv2.imshow("rotated card", new_bg)
        cv2.waitKey(0)

    def create_triple_card(self):
        pass


# Places the img onto the bigger image bg, in a random x,y coordinate
def place_card(img, bg, cords):
    height = bg.shape[0]
    width = bg.shape[1]
    if cords is None:
        # Generate random coordinates
        x_card = random.randint(0, width - img.shape[1])
        y_card = random.randint(0, height - img.shape[0])
    else:
        x_card, y_card = cords[:2]
    # Fill the bg rectangle created by the x,y coordinates with the img
    bg[y_card:y_card+img.shape[0], x_card:x_card+img.shape[1]] = img
    return bg, (x_card, y_card)


def main():
    newScene = Scene()
    while True:
        newScene.create_double_card()


if __name__ == "__main__":
    main()
