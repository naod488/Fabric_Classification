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

# To Run a model for training
This section assumes system has been set up according to the Project Report chapter 4 Methods System Setup
Make sure you use the appropriate dataset the model is ment for as explained in the section above
1. ensure my_utils.py is located in the same folder as the to run ipynb notebook file
2. remove the first 1 code block if runing on a local machine (remove the code to mount the google drive
3. update the file path variables to mach your environment 
(pathnames to update: 	variable "path" after the import in teh 3rd/2nd code block
						parameters for "checkpoint = my_utils.generate_callback(...,...)" after model.comple()
!Addtional notice!
when a model is trained the checkpoint will overwritte any file with the same path/name
in the user directory

# The CNN application (located in fabric_app)
The completed application in the fabric app folder is the python server implementation using flask,

Notes: a h5 file has already been located in the same folder as the executable
		it may be replace with any other h5 files but the variable for its path "MODEL" will be required to be changed approprietly,
		addtionally, if it was changed to a h5 file for the "fabrics_simple"
		dataset requires a change in the list variable called "TYPES"

to run:
- pip install, flask and tensorflow (or follow instructions in the Project Report Chapter 4 Methods System Setup)
- exectue the app.py file and wait for the console window to show "Running on "http://127.0.0.1:5000/"
- open the webbrowser and navigate to the "http://127.0.0.1:5000/"
from this point on the user will be shown a page with the option to upload an image, if done so
the user will be redirected to the results page, showing the outcome of the classification.
The image uploaded will be sorted on the hosting machine temporarely using a universally unique identifier to generate a unique filename to avoid concurrency issues
when multiple users upload an image with possibly the same name at the same time.

Addtional Notes:
3 Test files have been provided in "fabric_app" to submit as images:
- test_giberish.png should result in the user being notified of that it wasn't possible to classify the image
- test_giberish.txt should result in an alert to be displayed, if a user where to disable javascript and somehow upload the txt
  or any other non image file of their choosing, the user will be notified that it wasn't possible to classify the image
- test_Wool_ima_1.png (the fabrics dataset "Wool_ima_1.png"), the user will be presented with a classifcation result, in case of the
  original model configured it will present wool as the identifed fabric.

Limitations:
- The classifcation result does not have the option to label the image uploaded as none of the fabric types.
- The image to be classified is expted to possess a resolution of 400x400 for larger images, will be scaled down for evaluation,
  for that reason the image needs to be of a very high quality and close up, and possibly cropped.

There exist two alternate implementations, on using python tkinter and the other using node js,
these implementation are functionaly complete in terms of allowing an image to be loaded and classified.
To run:
- Tkinter: execute "fabric_app.py" libraries required view imports at the top of file source
- Node.js: execute the "node ." command within the folder after you see the host and port number displayed
  navigate to localhost:3000 (default configuration)
  
# Utility files
Dataset_Analysis('fabrics_...').ipynb:
Loads the images and displays a figure for the number of samples in each category by detecting the number of png files in each subfolder

my_utils.py:
a file with helper functions for the model creation notebook files, which is expected to be located with the same folder as the notebook files themselves

# Fair use
This project falls under fair use, results in the form of the fabrics dataset and datasets derived from this dataset and the trained model h5 files
are restricted for non-commercial use as by the author of the orignal dataset C. Kampouris et. al (2016)

# References
C. Kampouris, S. Zafeiriou, A. Ghosh, S. Malassiotis. The Fabrics Dataset. ibug.doc (2016). 
Available at: <https://ibug.doc.ic.ac.uk/resources/fabrics/> (Accessed: 14.02.2022)
