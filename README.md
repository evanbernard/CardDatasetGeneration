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

### Cropping Images
The script ImageExtract is used to automatically crop the base images into the image you want to place on different backgrounds. After running the script on our base images you'll be left with images in the CroppedImages folder looking something like this:


![CroppedImage](https://github.com/evanbernard/CardDatasetGeneration/blob/master/CroppedImages/S0.jpg)

Note that there is a variable in Settings.py called HORIZONTAL. When this is true, it will display the image so that the base is longer than the height. Also the cropped images are best when the base images are taken directly above the image, you can warp the image so that the image doesn't need to be directly above the object but in my case I had consistent base images so just cropping with ImageExtract.py worked well


The variables in Settings.py are used for testing this script and also toggles the saving of the images


Once you have the cropped images you'll need to label them. I used labelImg

### Pickles
CardImages.py and BackgroundImages.py are used to save and load pickle files. For the first run you'll need to run create_pickle() for both sets of images because we use the pickle files to save the images and load a random image. The pickle of images (not backgrounds) is a dictionary, so that we can extract the name of the image with the image.

### XML Parser
XMLParser.py is just a simple parser to grab the label coordinates of the cropped images. You can feed it the name of the image you need the coordinates for and it returns an array of arrays, each of the form [xmin, xmax, ymin, ymax]

### Scene Generation
SceneGeneration.py is the script that brings all the pieces together. You create a new instance of Scene and then call scene.generate_scene(n) where n is the number of images you want to place on the background, and should be kept to 6 or less to avoid accuracy issues. An example scene with n = 6 without displaying the labels:


![Scene No Labels](https://github.com/evanbernard/CardDatasetGeneration/blob/master/SceneExamples/noLabels.jpg)

An example scene with n = 6 displaying the labels:


![Scene With Labels](https://github.com/evanbernard/CardDatasetGeneration/blob/master/SceneExamples/withLabels.jpg)

If more than a third of a label is collectively covered by other images, then that label is not added to the final list of labels, as you can see by both of the 3 of spades labels showing but one of the 10 of spades label isn't. This is done to prevent a label being incorrect. Also if any part of the label is off the screen then it isn't added either.
