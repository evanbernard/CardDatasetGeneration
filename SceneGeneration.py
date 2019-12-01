from Constants import *
from BackgroundImages import Backgrounds
from CardImages import Cards
from CardExtractor import rotate_bound
from XMLParser import find_boxes


class Scene:
    def __init__(self):
        self.bg_images = Backgrounds()
        self.card_images = Cards()

    def create_single_card(self):
        # TODO when rotating the labels make sure you check to see if they're off the image
        #   if the are, then dont include that image in the training data
        new_bg = self.bg_images.get_random()

        # Our backgrounds are a little small, so apply a random resize
        random_size = random.uniform(1.5, 4)
        new_bg = cv2.resize(new_bg, (int(new_bg.shape[1]*random_size), int(new_bg.shape[0]*random_size)))
        # We will be resizing multiple times so we need to save our starting width and height so we know what size
        #   it should be at the end
        old_width = new_bg.shape[0]
        old_height = new_bg.shape[1]

        # Picks a random card, applies random brightness and contrast changes and returns the image in card and the
        #   image name in card_name
        card, card_name = self.card_images.get_random()

        # We need to randomly rotate the card on the background, so randomize the angle
        angle = random.randint(0, 360)

        # Note: if we were to rotate the card first then put it on the background we would have had either a cropped
        #   card or a card with black corners, which is no good, so we rotate the background instead
        # We first rotate the background by a random angle, note that rotate_bound will resize the image to make sure
        #   that the image doesn't get cropped at all (ie, it is sized up so that the corners aren't cut off)
        new_bg = rotate_bound(new_bg, angle, [])
        # Now that we have our rotated background, we can place a card vertically on that background with random
        #   coordinates, and return the new rotated background new_bg and the x,y location of the card position cords
        #   location
        new_bg, cords = place_card(card, new_bg, None)

        # We parse the xml file for the card chosen, to get an array of dictionaries, with each dict storing the cords
        bounding = find_boxes(card_name)
        # We extract the x and y min and max of the coordinates of the label
        xmin0, ymin0 = bounding[0]['xmin'] + cords[0], bounding[0]['ymin'] + cords[1]
        xmax0, ymax0 = bounding[0]['xmax'] + cords[0], bounding[0]['ymax'] + cords[1]
        xmin1, ymin1 = bounding[1]['xmin'] + cords[0], bounding[1]['ymin'] + cords[1]
        xmax1, ymax1 = bounding[1]['xmax'] + cords[0], bounding[1]['ymax'] + cords[1]

        # Now we need to rotate the background back to the original position so we have effectively rotated the card
        #   on the background, but we need to apply this rotation first to the coordinates
        pnts = rotate_bound(new_bg, -angle, [[xmin0, ymin0], [xmax0, ymax0], [xmin0, ymax0], [xmax0, ymin0],
                                             [xmin1, ymin1], [xmax1, ymax1], [xmin1, ymax1], [xmax1, ymin1]])
        new_bg = rotate_bound(new_bg, -angle, [])

        # Our points are now a numpy array of floats but we want an array of integer coordinates
        pnts = np.around(pnts.astype(int)).tolist()

        # We are left with an image with black borders of size old_width/2 because of the resizing, so lets grab the
        #   middle of the image to crop the black off, but first we need to apply this change to the coordinates
        for i in range(len(pnts)):
            pnts[i][0] -= int((new_bg.shape[1] - old_height) / 2)
            pnts[i][1] -= int((new_bg.shape[0] - old_width) / 2)
        # Now apply change to image
        new_bg = new_bg[int((new_bg.shape[0] - old_width)/2):int((new_bg.shape[0] + old_width)/2),
                        int((new_bg.shape[1] - old_height)/2):int((new_bg.shape[1] + old_height)/2)]


        xmin0 = int(min(pnts[i][0] for i in range(4)) * 2 / REDUCE)
        ymin0 = int(min(pnts[i][1] for i in range(4)) * 2 / REDUCE)
        xmax0 = int(max(pnts[i][0] for i in range(4)) * 2 / REDUCE)
        ymax0 = int(max(pnts[i][1] for i in range(4)) * 2 / REDUCE)

        xmin1 = int(min(pnts[i][0] for i in range(4, 8)) * 2 / REDUCE)
        ymin1 = int(min(pnts[i][1] for i in range(4, 8)) * 2 / REDUCE)
        xmax1 = int(max(pnts[i][0] for i in range(4, 8)) * 2 / REDUCE)
        ymax1 = int(max(pnts[i][1] for i in range(4, 8)) * 2 / REDUCE)


        new_bg = cv2.resize(new_bg, (int(new_bg.shape[1] * 2 / REDUCE), int(new_bg.shape[0] * 2 / REDUCE)))

        cv2.circle(new_bg, (xmin0, ymin0), 2, (255, 0, 255), -1)
        cv2.circle(new_bg, (xmin0, ymax0), 2, (255, 0, 255), -1)
        cv2.circle(new_bg, (xmax0, ymin0), 2, (255, 0, 255), -1)
        cv2.circle(new_bg, (xmax0, ymax0), 2, (255, 0, 255), -1)
        cv2.circle(new_bg, (xmin1, ymin1), 2, (255, 0, 255), -1)
        cv2.circle(new_bg, (xmin1, ymax1), 2, (255, 0, 255), -1)
        cv2.circle(new_bg, (xmax1, ymin1), 2, (255, 0, 255), -1)
        cv2.circle(new_bg, (xmax1, ymax1), 2, (255, 0, 255), -1)

        cv2.imshow("Single Scene", new_bg)
        cv2.waitKey(0)

    def create_double_card(self):
        new_bg = self.bg_images.get_random()

        # cv2.imshow("orig", new_bg)
        # Our backgrounds are a little small, so apply a random resize
        random_size = random.uniform(1.5, 4)
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

        new_bg = cv2.resize(new_bg, (int(new_bg.shape[1]*2/REDUCE),int(new_bg.shape[0]*2/REDUCE)))
        cv2.imshow("Double Scene", new_bg)
        cv2.waitKey(0)


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
    new_scene = Scene()
    while True:
        new_scene.create_single_card()


if __name__ == "__main__":
    main()
