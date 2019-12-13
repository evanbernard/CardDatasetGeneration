from Constants import cardFolder
import xml.etree.ElementTree as eT


# find_boxes(file) takes an xml file name such as S0 and returns a 2x4 array, where each row is in the format of
#   [xmin, xmax, ymin, ymax], representing the bounds of the label. There are 2 labels per card hence 2 rows
def find_boxes(file):
    tree = eT.parse(cardFolder + "\\" + file + ".xml")
    root = tree.getroot()
    bounds = []
    i = 0
    for obj in root.findall('object'):
        bounds.append([])
        bnd_box = obj.find('bndbox')
        x_min, y_min = int(bnd_box.find('xmin').text), int(bnd_box.find('ymin').text)
        x_max, y_max = int(bnd_box.find('xmax').text), int(bnd_box.find('ymax').text)
        bounds[i] = [x_min, x_max, y_min, y_max]
        i += 1
    return bounds
