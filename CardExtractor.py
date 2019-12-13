from Constants import *
from Settings import *


def main():
    img = cv2.imread(imFolder + "\\" + CARD_NAME + imExtension)
    # img_copy is the image we will be drawing contours on
    img_copy = img.copy()
    # width and height is the size we want our threshold to be if we show it
    width, height = int(img_copy.shape[1] / REDUCE), int(img_copy.shape[0] / REDUCE)
    # c is the largest area contour in the image
    c = find_largest_contour(img)

    # find the minimum bounding rectangle for the biggest contour
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    # Our goal with this box is to straighten it, then remove anything outside of it
    # After doing so we will be left with only the straightened and cropped image of the card
    if SHOW_CONTOURS:
        # This drawing of [box] is the minimum bounding rectangle around the contour we found, namely c
        cv2.drawContours(img_copy, [box], 0, (0, 255, 0), 2 * REDUCE)
        # This drawing of c is in red, and should be surrounding the card in the image copy
        cv2.drawContours(img_copy, c, -1, (0, 0, 255), 3 * REDUCE)

    # We need to rotate the box until it is straight, so we need to calculate theta; the angle of rotation
    theta = find_theta(box)
    # Next we perform the rotation on the corner points (the box)
    #print(box)
    box = rotate_bound(img_copy, theta, box)
    # Then we perform the rotation on the image
    img_copy = rotate_bound(img_copy, theta, [])

    # Our box is a numpy array of floats so we need to typecast to ints to make the points usable
    box = np.around(box.astype(int)).tolist()

    # Our new width and height for the image copy after we rotate it
    # The width and height need to be changed when rotating, otherwise the corners may be cropped after rotation
    nheight = int(img_copy.shape[0] / REDUCE)
    nwidth = int(img_copy.shape[1] / REDUCE)

    # We need two diagonal corners on the rotated image so that we can crop out everything outside of the box
    # Diagonal corners will always be found 2 indices apart, so either box[0] and box[2], or box[1] and box[3]
    p1 = box[2]
    p2 = box[0]

    # Crop everything in the image that is not within the two diagonal corner points p1 and p2
    result = crop_image(img_copy, p1, p2)

    # Resize the other images
    img_copy = cv2.resize(img_copy, (nwidth, nheight))
    orig = cv2.resize(img, (width, height))

    # We want the final size to be 300x420 so each card is consistent
    result = cv2.resize(result, IM_SIZE)

    if SHOW_DETAILS:
        cv2.imshow("Original", orig)
        cv2.imshow("Contours and Rotation", img_copy)

    if SHOW_IM:
        cv2.imshow("Result", result)
        cv2.waitKey(0)

    if EXPORT:
        cv2.imwrite(cardFolder + "\\" + CARD_NAME + imExtension, result)
        print("Added cropped file " + CARD_NAME + imExtension + " to the " + cardFolder + " folder.")


# crop_image(img_copy, p1, p2) takes an image and two points and returns the image found between p1 and p2
def crop_image(img, p1, p2):
    if SHOW_CONTOURS:
        # Display the 2 corner points we chose
        cv2.circle(img, (p2[0], p2[1]), 20, (255, 0, 255), -1)
        cv2.circle(img, (p1[0], p1[1]), 20, (255, 0, 255), -1)
    # Crops the image to be the rectangle from the diagonal corner points
    cropped_image = img[min(p2[1], p1[1]):max(p2[1], p1[1]), min(p2[0], p1[0]):max(p2[0], p1[0])]
    cropped_image = cv2.resize(cropped_image, (int(abs((p1[0] - p2[0]) / REDUCE)), int(abs((p1[1] - p2[1]) / REDUCE))))
    return cropped_image


# find_largest_contour(img) takes in an image img, and returns the largest area contour
def find_largest_contour(img):
    # Blurring the image to get rid of the noise, making the contours more accurate
    img_blur = cv2.bilateralFilter(img, d=12, sigmaSpace=75, sigmaColor=75)
    # Convert the blurred image to grayscale
    gray = cv2.cvtColor(img_blur, cv2.COLOR_RGB2GRAY)
    # Apply the threshold
    a = gray.max()
    _, thresh = cv2.threshold(gray, a/2 + 60, a, cv2.THRESH_BINARY)
    # Get the contours using the threshold image, then grab the largest one
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    if SHOW_DETAILS:
        thresh = cv2.resize(thresh, (int(img.shape[1]/REDUCE), int(img.shape[0]/REDUCE)))
        cv2.imshow("Threshold", thresh)

    # c is the maximum contour, and hopefully the contour surrounding only the card
    c = max(contours, key=cv2.contourArea)
    return c


# find_theta(box) takes in a box (4 coordinates which form a rectangle), and outputs the angle of which we need to
#   rotate the box in order to straighten the box such that the smallest sides are on the bottom and the top
#   ie. if the box was around a playing card, theta will be the angle we need to rotate the card to make it upright
def find_theta(box):
    # We need two corner points of the box to calculate theta, and we want the card to be oriented so that its width
    #   is smaller than its height, so we can choose any corner p1, then the corner closest to p1, ie, the minimum
    #   distance. We only need to check corners 1 and 3 because corner 4 is diagonal to corner 0
    p1 = box[0]
    dist1 = math.sqrt((box[1][0] - p1[0]) ** 2 + (box[1][1] - p1[1]) ** 2)
    dist3 = math.sqrt((box[3][0] - p1[0]) ** 2 + (box[3][1] - p1[1]) ** 2)

    if dist1 < dist3:
        if HORIZONTAL:
            p2 = box[3]
        else:
            p2 = box[1]
    else:
        if HORIZONTAL:
            p2 = box[1]
        else:
            p2 = box[3]

    # Once we have our 2 corner points, we just use some basic geometry to calculate the angle
    theta = math.atan((p1[1] - p2[1]) / (p2[0] - p1[0])) * 180 / math.pi
    return theta


# rotate_bound(image, angle, points) takes in an image image, and angle angle and some array of coordinates points
# if points is empty, it only rotates the image and returns that rotated image, otherwise it will return the rotated
#   points
def rotate_bound(image, angle, points):
    # Find the dimensions of the image and then find the center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # Find the rotation matrix (applying the negative of the angle to rotate clockwise), then find the sine and cosine,
    #   which are the rotation components of the matrix
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # Calculate the new size of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # Adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    if not len(points):
        # There are no points, so we need to return the rotated image
        return cv2.warpAffine(image, M, (nW, nH))
    else:
        # Add 1's to the points matrix to make the dot product possible, then dot the points with the rotation matrix
        #   and return the rotated points
        ones = np.ones(shape=(len(points), 1))
        points_ones = np.hstack([points, ones])
        return M.dot(points_ones.T).T


if __name__ == "__main__":
    if TESTING_EXTRACT:
        SHOW_IM = True
        SHOW_CONTOURS = True
        SHOW_DETAILS = True
        ALL_CARDS = True
    elif EXPORT_EXTRACT:
        SHOW_IM = False
        SHOW_CONTOURS = False
        SHOW_DETAILS = False
        ALL_CARDS = True
        EXPORT = True

    if ALL_CARDS:
        for im in os.listdir(imFolder):
            # This assumes the name of the cards are in the format {suit}{value}
            #   and that 10 is treated as 0 (so all card names are exactly 2 characters long)
            CARD_NAME = im[:len(im)-len(imExtension)]
            main()
    else:
        main()
