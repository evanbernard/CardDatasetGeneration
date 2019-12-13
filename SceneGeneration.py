from Constants import *
from BackgroundImages import Backgrounds
from CardImages import Cards
from CardExtractor import rotate_bound
from XMLParser import find_boxes
from Settings import REDUCE


class Scene:
    def __init__(self):
        self.bg_images = Backgrounds()
        self.card_images = Cards()
        # final_boxes is a dictionary full of each card in the image, the keys are the image names
        #   and the values are of the form [[xmin0, xmax0, ymin0, ymax0][xmin1, xmax1, ymin1, ymax1]]
        #   we need two sets because each set represents the box around the card corner with the info on it,
        #   and there are at most 2 of those we need to keep track of
        self.final_boxes = {}

    def create_scene(self, num_cards):
        self.final_boxes = {}
        card_bounds_dict = {}
        new_bg = self.bg_images.get_random()

        # Our backgrounds are a little small, so apply a random resize
        random_size = random.uniform(1.5, 3)
        new_bg = cv2.resize(new_bg, (int(new_bg.shape[1]*random_size), int(new_bg.shape[0]*random_size)))
        # We will be resizing multiple times so we need to save our starting width and height so we know what size
        #   it should be at the end
        old_width = new_bg.shape[0]
        old_height = new_bg.shape[1]

        # Loop through num_cards times to add num_cards cards to the scene, adding more than ~6 cards to the scene
        #   starts to slightly blur the cards that were first placed in the scene because of the many resizings of
        #   the image, which is great for improving the model's accuracy on blurry images of cards, but it also
        #   slightly offsets the label coordinates the more cards we have because the coordinates need to be ints, so
        #   we have to round the coordinates after rotating the image, which after enough times can have a significant
        #   impact to the coordinates of some of the labels
        for i in range(num_cards):
            # Picks a random card, applies random brightness and contrast changes and returns the image in card and the
            #   image name in card_name

            card, card_name = self.card_images.get_random()
            # since we are dealing with a dictionary, having a duplicate name will remove any labels for one of the
            #   duplicate cards, so it's better to just choose a different card if it's a duplicate
            while card_name in self.final_boxes:
                card, card_name = self.card_images.get_random()
            # We need to randomly rotate the card on the background, so randomize the angle
            angle = random.randint(0, 360)

            # Note: if we were to rotate the card first then put it on the background we would have had either a cropped
            #   card or a card with black corners, which is no good, so we rotate the background instead
            # We first rotate the background by a random angle, note that rotate_bound will resize the image to make
            #   sure that the image doesn't get cropped at all (ie, it is sized up so that the corners aren't cut off)
            new_bg = rotate_bound(new_bg, angle, [])
            # Now that we have our rotated background, we can place a card vertically on that background with random
            #   coordinates, and return the new rotated background new_bg and the x,y location of the card position
            #   cords location
            new_bg, cords, card_bounds = place_card(card, new_bg)

            # We parse the xml file for the card chosen, to get an array in the format of
            #   [[xmin, xmax, ymin, ymax], [xmin, xmax, ymin, ymax]]
            bounding = find_boxes(card_name)
            bounding = add_starting_loc(bounding, cords[0], cords[1])

            # We extract the x and y min and max of the coordinates of the label and the card boundaries
            xmin0, xmax0, ymin0, ymax0 = bounding[0]
            xmin1, xmax1, ymin1, ymax1 = bounding[1]
            cxmin, cxmax, cymin, cymax = card_bounds

            # Now we need to rotate the background back to the original position so we have effectively rotated the card
            #   on the background, but we need to apply this rotation first to all of the corners
            points = rotate_bound(new_bg, -angle, [[xmin0, ymin0], [xmax0, ymax0], [xmin0, ymax0], [xmax0, ymin0],
                                                   [xmin1, ymin1], [xmax1, ymax1], [xmin1, ymax1], [xmax1, ymin1]])
            ncard_bounds = rotate_bound(new_bg, -angle, [[cxmin, cymin], [cxmax, cymin],
                                                         [cxmax, cymax], [cxmin, cymax]])
            # Now that we rotates the coordinates we can rotate the image back to it's original position
            new_bg = rotate_bound(new_bg, -angle, [])

            # Our points are a numpy array of floats but we want an array of integer coordinates
            points = np.around(points.astype(int)).tolist()
            ncard_bounds = np.around(ncard_bounds.astype(int)).tolist()

            # TODO FIGURE OUT HOW THIS MAKES SENSE???? WE'RE SUBTRACTING THE HEIGHT FROM THE WIDTH AND VICE VERSA
            #  AND IT DOESN'T WORK OTHERWISE??? bg.shape[0] is the height but when I wrote it I thought it was width??
            # ----------------------------------------------------------------------------------------------------------
            # We are left with an image with black borders of size old_width/2 because of the resizing, so lets grab the
            #   middle of the image to crop the black off, but first we need to apply this change to the coordinates
            for i in range(len(points)):
                points[i][0] -= int((new_bg.shape[1] - old_height) / 2)
                points[i][1] -= int((new_bg.shape[0] - old_width) / 2)
            for j in range(len(ncard_bounds)):
                ncard_bounds[j][0] -= int((new_bg.shape[1] - old_height) / 2)
                ncard_bounds[j][1] -= int((new_bg.shape[0] - old_width) / 2)
            # Now apply change to image
            new_bg = new_bg[int((new_bg.shape[0] - old_width)/2):int((new_bg.shape[0] + old_width)/2),
                            int((new_bg.shape[1] - old_height)/2):int((new_bg.shape[1] + old_height)/2)]
            # ----------------------------------------------------------------------------------------------------------

            # calculate the min and max of the points after rotation, and we will be dividing the size of the im
            #   by REDUCE / 2, so we need to make those adjustments to the points now
            xmin0 = int(min(points[i][0] for i in range(4)) * 2 / REDUCE)
            ymin0 = int(min(points[i][1] for i in range(4)) * 2 / REDUCE)
            xmax0 = int(max(points[i][0] for i in range(4)) * 2 / REDUCE)
            ymax0 = int(max(points[i][1] for i in range(4)) * 2 / REDUCE)

            xmin1 = int(min(points[i][0] for i in range(4, 8)) * 2 / REDUCE)
            ymin1 = int(min(points[i][1] for i in range(4, 8)) * 2 / REDUCE)
            xmax1 = int(max(points[i][0] for i in range(4, 8)) * 2 / REDUCE)
            ymax1 = int(max(points[i][1] for i in range(4, 8)) * 2 / REDUCE)

            for point in range(len(ncard_bounds)):
                for k in range(2):
                    ncard_bounds[point][k] = int(ncard_bounds[point][k] * 2 / REDUCE)

            p1, p2, p3, p4 = (ncard_bounds[i] for i in range(4))
            card_bounds_dict[card_name] = [p1, p2, p3, p4]
            self.final_boxes[card_name] = [[xmin0, xmax0, ymin0, ymax0], [xmin1, xmax1, ymin1, ymax1]]

        # remove all covered labels and labels that are partially off or completely off the screen
        new_bg = cv2.resize(new_bg, (int(new_bg.shape[1] * 2 / REDUCE), int(new_bg.shape[0] * 2 / REDUCE)))
        self.final_boxes = exposed_labels(self.final_boxes, card_bounds_dict, new_bg.shape[1], new_bg.shape[0])

        for key in self.final_boxes:
            for i in range(2):
                if self.final_boxes[key][i]:
                    cv2.rectangle(new_bg, (self.final_boxes[key][i][0], self.final_boxes[key][i][3]),
                                          (self.final_boxes[key][i][1], self.final_boxes[key][i][2]), (255, 0, 0), 1)

        cv2.imshow("Scene", new_bg)
        print(self.final_boxes)
        cv2.waitKey(0)


# Places the img onto the bigger image bg, in a random x,y coordinate
def place_card(img, bg):
    height = bg.shape[0]
    width = bg.shape[1]
    x_card = random.randint(0, width - img.shape[1])
    y_card = random.randint(0, height - img.shape[0])

    card_extremes = [x_card, x_card + img.shape[1], y_card, y_card + img.shape[0]]

    # Fill the bg rectangle created by the x,y coordinates with the img
    bg[card_extremes[2]:card_extremes[3], card_extremes[0]:card_extremes[1]] = img
    return bg, (x_card, y_card), card_extremes


# intersecting_area will take in two randomly rotated shapes and output the area that is intersecting both shapes.
#   For this implementation we only will feed it rectangles but it will work on any 2 shapes. It will sweep from
#   left to right, calculating the number of pixels in both shapes for each column of pixels.
#   last column will be the column number that has the maximum x value out of rect1 and rect2
def intersecting_area(rect1, rect2):
    # rect1 is of the form [p1, p2, p3, p4] where each p is [x, y]
    # rect2 is of the form [xmin, xmax, ymin, ymax]
    # lox has the first 4 values being xvalues of rect1 and last 2 being xvalues of rect2, similarly for loy
    x1, x2, x3, x4 = ((rect1[i][0] for i in range(4)))
    x5, x6 = (rect2[i] for i in range(2))
    lox = [x1, x2, x3, x4, x5, x6]
    y1, y2, y3, y4 = ((rect1[i][1] for i in range(4)))
    y5, y6 = (rect2[i] for i in range(2, 4))
    loy = [y1, y2, y3, y4, y5, y6]

    # if r1_right is true, then all the x coordinates of the card boundary (rect1) are strictly greater than that of
    #   the label, so there is no way the label intersects with the card, so we return 0. do it for each direction
    r1_right = all(lox[i] > lox[4] for i in range(4)) and all(lox[i] > lox[5] for i in range(4))
    r1_left = all(lox[i] < lox[4] for i in range(4)) and all(lox[i] < lox[5] for i in range(4))
    r1_under = all(loy[i] < loy[4] for i in range(4)) and all(loy[i] < loy[5] for i in range(4))
    r1_above = all(loy[i] > loy[4] for i in range(4)) and all(loy[i] > loy[5] for i in range(4))

    if r1_right or r1_left or r1_under or r1_above:
        return 0

    overlap_area = 0
    # step through each 2x2 area of 'pixels' in the label, check if one of those pixels is inside the boundaries of the
    #   card (rect1), if it is inside rect1, then add 4 to the area of overlapping since we assume all 4 pixels are in
    #   it. Note: it is more accurate if we iterate over every pixel, but doing it in groups of 2x2 makes it 4x
    #   more efficient and doesn't affect accuracy enough to make a difference in our application here
    for x in range(rect2[0], rect2[1], 2):
        for y in range(rect2[2], rect2[3], 2):
            if point_inside_polygon(x, y, rect1):
                overlap_area += 4
    # actual_area = (rect2[1] - rect2[0])*(rect2[3] - rect2[2])
    return overlap_area


# point_inside_polygon(x, y, poly) returns true if the point (x, y) is inside the polygon poly, where poly is an
#   ordered list of corners of the polygon. ordered in the sense that it is either counter clockwise or clockwise,
#   so you always know there exists a line between p subscript i and p subscript i+1
def point_inside_polygon(x, y, poly):
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


# add_starting_loc(boxes, x_start, y_start) boxes is in the form [[xmin0, xmax0, ymin0, ymax0],
#   [xmin1, xmax1, ymin1, ymax1]] and the x starting point and y starting point of both boxes. It adds the x starting
#   point to all the x coordinates and similarly for y. This is used when we have the coordinates of the labels for
#   a cropped card and we put the card on the random background in a random position, this gives us the updated label
#   positions
def add_starting_loc(boxes, x_start, y_start):
    for i in range(2):
        for u in range(2):
            boxes[i][u] += x_start
        for u in range(2):
            boxes[i][u + 2] += y_start
    return boxes


# exposed_labels(labels, card_bounds, xmax, ymax) returns all the labels in the labels dict that gets passed to it that
#   are not more than one third covered by another card or off the screen at all, where xmax and ymax are the max screen
#   coordinates
def exposed_labels(labels, card_bounds, width, height):
    new_bounds = card_bounds
    # labels is a dictionary so we want to iterate through each label
    for key in labels:
        card = card_bounds[key]
        i = 0
        # since we're grabbing the label from the card called key, we don't want to check for overlapping between the
        #   label and the card that the label is for, since obviously it will think the label is covered by the card
        del new_bounds[key]
        # the label dict has two labels [xmin, xmax, ymin, ymax] and we need to iterate over each one
        for value in labels[key]:
            # first check to see if the label is completely inside the image based on the width and height of the image
            if labels[key][i][0] > width or labels[key][i][0] < 0 or \
                    labels[key][i][1] > width or labels[key][i][1] < 0:
                labels[key][i] = []
            elif labels[key][i][2] > height or labels[key][i][2] < 0 or \
                    labels[key][i][3] > height or labels[key][i][3] < 0:
                labels[key][i] = []
            else:
                # if the label is completely inside the image, we need to find the overlapping area of that label
                #   and each card boundaries that is not the same card as the label. Since the dictionaries are sorted
                #   the label in position i will never be covered by any cards with position less than i
                # Also since we deleted the card boundary of the card attached to the label and there are no recurring
                #   cards in the dictionary, each card in new_bounds has the potential of covering the card
                overlap_amount = 0
                # We keep track of the total overlapping amount of the label, but we take the safe route and assume
                #   that any overlapping area between the label and a card is distinct
                # Doing it this way avoids the issue of including a label that is slightly covered by a bunch of other
                #   cards, where together the label is completely covered but no one card covers it enough to remove
                #   the label from the dictionary, so by adding the overlapping amount for each card will sometimes
                #   remove a label that isn't completely covered but at least we know we won't have an incorrect label
                for card2 in new_bounds:
                    overlap_amount += intersecting_area(card_bounds[card2], value)
                    # label_size is the actual area of the label we're checking for overlaps
                    label_size = (value[1] - value[0]) * (value[3] - value[2])
                    # if more than a third of the label is covered by one of the cards, then we don't want to
                    #   include that label in the data set, since it's likely completely unidentifiable
                    if label_size / 3 < overlap_amount:
                        labels[key][i] = []
            i += 1
    return labels


def main():
    new_scene = Scene()
    while True:
        new_scene.create_scene(6)


if __name__ == "__main__":
    main()
