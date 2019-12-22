# Dataset Generation
The goal of this project is to generate a dataset of random cards rotated and placed in a random way on a random background, while keeping track of the labels on the cards. Running SceneGeneration.py will produce as many images as you specify, where each image contains the number of cards you specify, and it will also generate a .txt file that lists all the image names and labels and coordinates in each image.

Though this project was created with cards in mind, it will work for generating a dataset with any rectangular image or any image with some modifications to the scripts. This dataset generation is useful if you need a dataset of some images on different backgrounds with random changes being made to the images, like lighting, rotations, position and contrast. 

## Getting Started
### Prerequisites

The packages this project uses:

```
imutils==0.5.3
numpy==1.17.4
opencv-python==4.1.2.30
pickle-mixin==1.0.2
```
You'll need to place your base images in the Images folder,  an example of a base image for the card dataset can be seen here:


![BaseImage](https://github.com/evanbernard/CardDatasetGeneration/blob/master/Images/S0.jpg)

## Cropping Images
The script ImageExtract is used to automatically crop the base images into the image you want to place on different backgrounds. After running the script on our base images you'll be left with images in the CroppedImages folder looking something like this:


![CroppedImage](https://github.com/evanbernard/CardDatasetGeneration/blob/master/CroppedImages/S0.jpg)

Note that there is a variable in Settings.py called HORIZONTAL. When this is true, it will display the image so that the base is longer than the height. Also the cropped images are best when the base images are taken directly above the image, you can warp the image so that the image doesn't need to be directly above the object but in my case I had consistent base images so just cropping with ImageExtract.py worked well


The variables in Settings.py are used for testing this script and also toggles the saving of the images


Once you have the cropped images you'll need to label them. I used labelImg

## Pickles
CardImages.py and BackgroundImages.py are used to save and load pickle files. For the first run you'll need to run create_pickle() for both sets of images because we use the pickle files to save the images and load a random image. The pickle of images (not backgrounds) is a dictionary, so that we can extract the name of the image with the image.

## XML Parser
XMLParser.py is just a simple parser to grab the label coordinates of the cropped images. You can feed it the name of the image you need the coordinates for and it returns an array of arrays, each of the form [xmin, xmax, ymin, ymax]

## Scene Generation
### What Do You Need To Run This?
To run this script, you need to have the following:
* 2 pickle files
  * One full of random background images (retrieved by calling Backgrounds()) 
  * One containing a dictionary, with the keys being the name of the image, and the values being the actual image of the card (these cards will be randomly placed onto the randomly chosen background image, so the images should be cropped, which ImageExtractor.py does automatically for you, and the contents of the pickle file are retrieved by calling Cards())
* An xml file for each cropped image containing the label of the important parts of the image (in the case of cards the xml files contain the bounding boxes for the two identifying corners of the cards). The xml files should be named {classifier_name}.xml and should be in the croppedImages folder.

### What Does It Do?
SceneGeneration.py is the script that brings all the pieces together. You create a new instance of Scene and then call
```Python
generate_images(scene, train, num)
```
This will create num many images, each with a random number of cards (between 1 and 6) on each image. The number of cards is kept to less than 7 becuase at 7 cards, the rotation of the label coordinates with rounding may slightly offset the position of the labels. The parameter train is a boolean and it's what determines where the images are saved. If train = True, then the images will be stored in the train folder, and they'll be stored in the test folder otherwise. You should call generate_images twice, once with train = True and once with train = False, typically the number of testing images is 10% of the number of training images. An example scene with n = 6 without displaying the labels:


![Scene No Labels](https://github.com/evanbernard/CardDatasetGeneration/blob/master/SceneExamples/noLabels.jpg)

An example scene with n = 6 displaying the labels:


![Scene With Labels](https://github.com/evanbernard/CardDatasetGeneration/blob/master/SceneExamples/withLabels.jpg)

If more than a third of a label is collectively covered by other images, then that label is not added to the final list of labels, as you can see by both of the 3 of spades labels showing but one of the 10 of spades label isn't. This is done to prevent a label being incorrect. Additionally, if any part of the label is off the screen, the label is not added.

In order to use the label data with a yolov3 implementation for object detection, we need the label coordinates and images in a specific format in a text file called CLASS_test and CLASS_train. For each image generated by generate_images, a line is entered into CLASS_train or CLASS_test, depending on if the image is a training image or a testing image. The line in the text file is formatted as follows:
```
DRIVE:/path/to/image/train/n.jpg xmin ymin xmax ymax classifier_num xmin ymin xmax ymax classifier_num ...
```
The path is the path to the image, and {x, y}{min, max} are the coordinates of one label of a card, and classifier_num is line in classifers.txt which corresponds to the object the label is bounding. For example, if we have a test image with only one label, and that label is in the top left corner of the screen bounding a 2 of hearts (the first line in classifiers.txt is H2, which is the 2 of hearts), then the line in CLASS_test corresponding to that image would look as follows:
```
DRIVE:/path/to/image/test/n.jpg 0 0 10 20 0
```
Here, the width of the label is 10, the height 20, and the label is bounding the 2 of hearts, since the 0th line in classifiers.txt is H2.
