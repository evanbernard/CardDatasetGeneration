from Constants import cardFolder
import xml.etree.ElementTree as eT


# find_boxes(file) takes an xml file name such as S0 and returns an array of 2 dictionaries, where each dictionary
#   represents a bounding box for that file, with the name of the card, and x and y min and max values
def find_boxes(file):
    tree = eT.parse(cardFolder + "\\" + file + ".xml")
    root = tree.getroot()
    boxes = []
    i = 0
    for obj in root.findall('object'):
        boxes.append({})
        name = obj.find('name').text
        boxes[i]['name'] = name

        bnd_box = obj.find('bndbox')
        x_min, y_min = int(bnd_box.find('xmin').text), int(bnd_box.find('ymin').text)
        x_max, y_max = int(bnd_box.find('xmax').text), int(bnd_box.find('ymax').text)

        boxes[i]['xmin'], boxes[i]['ymin'] = x_min, y_min
        boxes[i]['xmax'], boxes[i]['ymax'] = x_max, y_max
        i += 1
    return boxes

