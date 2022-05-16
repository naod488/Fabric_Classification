from flask import Flask, request, render_template, Markup

import tensorflow as tf
import os
import numpy as np
from uuid import uuid1

APP = Flask(__name__)

MODEL = tf.keras.models.load_model("Model-4a-Aug-fa.h5")
TYPES = ['Cotton', 'Denim', 'Nylon', 'Polyester', 'Silk', 'Wool']

TYPE_INFO_DICT = {
    # information obtained from Robert Jameson on www.fabricfits.com/how-to-tell-if-fabric-is-100-cotton/
    "Cotton": Markup("""Real Cotton, easiliy the most used fabric, is light, soft and breathable.<br>
                        It is also quite stiff and easily wrinkles when you pinch a corner
                        or fold it.<br>
                        When burned it smells like burnt paper and will have an orange afterglow
                        with the ashes being dissolvable in water."""),
    # information obtained from the sewport support team on www.sewport.com/fabrics-directory/denim-fabric
    "Denim": Markup("""Denim is a subcattegorie of regular cotton.<br>
                        It can be identified by the intervowen structure of dyed and uncolored threads,
                        is woven using dense threads and is not or only very slightly strechy."""),
    # all of the below information provided by James V.
    #  on www.sewingiscool.com/how-to-identify-fabrics/
    "Nylon": Markup("""Nylon is simlar to Polyester by feeling artifical.
                        It can be strectched further than most other fabrics, and to further
                        test weither it is nylon or another similar fabric like pyester
                        a wather test can be conducted, where the nylon fabric should absorg more water."""),
    "Polyester": Markup("""Polyester used to be very artificial looking and feeling fabric, 
                            this has slightly improved with the manufacturing process.
                            When held up to a light source its texture should remain constant.
                            The weave structure is ordered, symmetrical and even in a robotic fashion,
                            which is distinct from natural fibres such as cotton."""),
    "Silk": Markup("""Silk is a very flexible and smoth material.<br>
                        Rubing the fabric should produce a warm fell, and rubing it against itself 
                        should produce little friction like it is gliding against itself."""),
    "Wool": Markup("""Wool is a very warm, durable and easy to care for fabric.<br>
                        To make certain that a piece of fabric is of wool, one may
                        perfrom a bleach test, this involves soaking a bit of the fabric
                        in bleach for about 8 hours, by the end the fabric should be almost
                        completely disolve.
                        A felt test can be performed where if the fabric pulls appart
                        after being made wet and shoved together, then it is not wool.""")
}

def predict(save_path: str):
    #based of https://www.tensorflow.org/tutorials/images/classification
    imgSize = (400, 400)
    img = tf.keras.preprocessing.image.load_img(
        save_path, target_size=imgSize)
    
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis

    pred = MODEL.predict(img_array)
    
    score = tf.nn.softmax(pred[0])
    result = f"This image most likely belongs to {TYPES[np.argmax(score)]} with a predictive power of {np.round(100 * np.max(score), 2)}%."
    return result, score

def showConfidence(predictions):
    counts = 0
    valuePairs = []
    for val in predictions[0:6]:
        pair = []
        pair.append(TYPES[counts]) 
        pair.append(np.round(100 * float(val), 2))
        counts += 1
        
        valuePairs.append(pair)

    print(valuePairs)
    valuePairs.sort(key=lambda x: x[1], reverse=True)

    outputValues = []
    for pair in valuePairs:
        outputValues.append(f"{pair[0]}: {pair[1]}%")

    return outputValues

def open_img(name: str):
    #display the calssification results
    result, predictions = predict(name)

    #variable for the classification type
    predType = TYPES[np.argmax(predictions)]

    #display the confidence values for the other options
    values = showConfidence(predictions)
    
    #return result, values, predictions
    return result, predType, values

@APP.route('/')
def home():
    intro_Text = Markup("""This website is the image classifier produced by Nathan Odibo 
                    for the dissertation project at City, University of london.<br>
                    <br>
                    The classifier uses a convolutional neural network for the purposes of
                    image classification.<br>
                    It possess the ability to distinguish among 6 fabrics 
                    [Cotton, Denim, Nylon, Polyester, Silk, Wool].<br>
                    <br>
                    To record and upload your image ensure that the image is close up, as sharp as possible and of 400x400 resolution, 
                    or croped down to the specified resolution from a larger image, 
                    it should be taken looking straight at the fabric with no direct shadow or light obscuring the image.<br>
                    For examples on how images should look like visit www.ibug.doc.ic.ac.uk/resources/fabrics/.<br>
                    <br>
                    Limitations:<br>
                    The default model confirgured for use for this web application is a convolutional neural network that has achieved
                    an over 75 precent accuracy on the validation split of the dataset it was trained on, provided on www.ibug.doc.ic.ac.uk/resources/fabrics/,<br>
                    as such the models shows to the environment in which the original data is taken in am struggles to perform well on custom data
                    showing an accuracy of ~25 on a set of 22 images of cotton fabrics, 11 taken by a Sony camera and phone each.<br>
                    Therefore major caution is advised when relying on the results provided by this module on custom data.<br>
                    <br>
                    Operation:<br>
                    <ul>
                    <li>Use the file selector below to select a .jpg or .png (recommended) image
                    on your device.</li>
                    <li>Press the upload button.</li>
                    <li>If no errors occurred you will be shown the classification results for the
                    uploaded image in the form of a % which indicates, of the identifiable fabrics,
                    which image has the largest likelihood to be of a certain fabric.</li>
                    <li>In addtion to that a short summary will be provided on how you can perform a test to
                    be certain that the fabric was corretly identified.</li>
                    </ul>""")
    return render_template('index.html', prediction_text="", information_text = intro_Text, result_data="")

@APP.route('/result', methods=['POST'])
def predict_request():
    # Get file and save it
    file = request.files['filetoupload']

    # Generate a filename using a universally unique identifier based on the system and local time
    filename = str(uuid1()) + ".png"

    file.save(filename)

    # classifiy the image and obtain the results
    try:
        prediction, predType, results = open_img(filename)
        predTypeText = TYPE_INFO_DICT[predType]
    except:
        prediction = "An error occured, the image could not be classified"
        predTypeText = ""
        results = ""
    # delete the image from the system
    os.remove(filename)

    # send the updated html response
    return render_template('index.html', prediction_text=prediction, information_text = predTypeText, result_data=results)


if __name__ == "__main__":
    #APP.run(host='0.0.0.0', port=3000)
    APP.run(debug=True)