# Fabric_Classification
A Convolutional Neural Network (CNN) fabric classification model creation and application deployment project

This folder ontains various ipynb files setup for a google collab environment, h5 files for trained models, some utility files, and a folder containing various
implementations for a tkinter, node.js and python flask for a CNN image classification applications.

# Model creation notebook ipynb files, trained models saves h5 files and datasets
The project consists of several 4 layer models that classifies bettween 2 or 6 images of depending on the Model version
Models version 1 a 2 layer model to classify image of Denim and Wool
Models version 2 is a 4 layer model which also classifies images of Denim and Wool
Models version 3 is a 4 layer model which classifies images of Cotton, Denim, Nylon, Polyester, Silk and Wool
Models version 4 is a 6 layer model which classifies images of Cotton, Denim, Nylon, Polyester, Silk and Wool

The datasets are: 
fabrics_adjusted: A dataset consisting of fabric types Cotton (), Denim (), Nylon (), Polyester (), Silk () and Wool (), selected from the original dataset (link below) 
on the basis of the number of samples and omitting irrelevant categories
(used for models version 3 and 4)

fabrics_simple: A dataset consisting of fabric types Denim () and Wool (), from the fabrics_adjusted dataset on the basis of the number of samples
(used for models version 1 and 2)

The original complete fabrics dataset can be obtained from:
Fabrics: the original datasete is vailable at https://ibug.doc.ic.ac.uk/resources/fabrics/

Datasets for the ipynb files and h5 for the trained models in the corresponding ipynb files are available on the authors google drive:
https://drive.google.com/drive/folders/1afrvWWTIm5FQYpH1wWQzKZMVMjSxsGtx?usp=sharing

# The CNN application
The completed application in the fabric app folder is the python server implementation using flask,
to run:
- pip install, flask and tensorflow
- exectue the app.py file and wait for the console window to show "Running on "http://127.0.0.1:5000/"
- open the webbrowser and navigate to the "http://127.0.0.1:5000/"
from this point on the user will be shown a page with the option to upload an image, if done so
the user will be redirected to the results page, showing the outcome of the classification.
The image uploaded will be sorted on the hosting machine temporarely using a universally unique identifier to generate a unique filename to avoid concurrency issues
when multiple users upload an image with possibly the same name at the same time.

Limitations:
- The classifcation result does not have the option to label the image uploaded as none of the fabric types.
- The image to be classified is expted to possess a resolution of 400x400 for larger image, only the top left 400x400 pixels are evaluated,
  for that reason the image needs to be a very close up shoot roughly 6cm distance zoomed in dependent on kamera quality.
  (see one of the datasets for reference)

# Utility files
Dataset_Analysis(...).ipynb:
Loads the images and displays a figure for the number of samples in each category by detecting the number of png files in each subfolder

my_utils.py:
a file with helper functions for the model creation notebook files, which is expected to be located with the same folder as the notebook files themselves

model_loader.ipynb:
Allows to load custom datasets and perform a mass prediction on them with a model specified by a model path

# Fair use
This project falls under fair use, results in the form of the fabrics dataset and datasets derived from this dataset and the trained model h5 files
are restricted for non-commercial use as by the author of the orignal dataset C. Campouris et. al (2016)

# References
C. Kampouris, S. Zafeiriou, A. Ghosh, S. Malassiotis. The Fabrics Dataset. ibug.doc (2016). 
Available at: <https://ibug.doc.ic.ac.uk/resources/fabrics/> (Accessed: 14.02.2022)
