from flask import Flask, request, render_template, Markup

import tensorflow as tf
import os
import numpy as np
from uuid import uuid1

APP = Flask(__name__)

MODEL = tf.keras.models.load_model("a_model_Aug_V5.h5")
TYPES = ['Cotton', 'Denim', 'Nylon', 'Polyester', 'Silk', 'Wool']

TYPE_INFO_DICT = { 
    "Cotton": Markup("""Cotton is"""),
    "Denim": Markup("""Denim is"""),
    "Nylon": Markup("""Nylon is"""),
    "Polyester": Markup("""Polyester is"""),
    "Silk": Markup("""Silk is"""),
    "Wool": Markup("""Wool is""")
}


def predict(save_path: str):
    #try:
        imgSize = (400, 400)
        img = tf.keras.preprocessing.image.load_img(
            save_path, target_size=imgSize)
        
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create batch axis

        pred = MODEL.predict(img_array)
        
        score = tf.nn.softmax(pred[0])
        result = f"This image most likely belongs to {TYPES[np.argmax(score)]} with a predictive power of {np.round(100 * np.max(score), 2)}%."
        return result, score
    
    #except Exception as e:
    #    return "Image invalid: " + str(e), ""

def showConfidence(predictions):
    #try:
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

    #except Exception as e:
    #    return "Image invalid: " + str(e)

def open_img(name: str):
    #try:
        #display the calssification results
        result, predictions = predict(name)

        #variable for the classification type
        predType = TYPES[np.argmax(predictions)]

        #display the confidence values for the other options
        values = showConfidence(predictions)
        
        #return result, values, predictions
        return result, predType, values
    #except Exception as e:
    #    return "An error occured" + str(e), "unable to classifiy the image", [""]


@APP.route('/')
def home():
    intro_Text = Markup("""This website is the image classifier produced by Nathan Odibo 
                    for the dissertation project at City, University of london.<br>
                    <br>
                    The classifier uses a convolutional neural network for the purposes of
                    image classification.<br>
                    It possess the ability to distinguish among 6 fabrics 
                    [Cotton, Denim, Nylon, Polyester, Silk, Wool], with the limitation of an 
                    inability to classify a fabric as none 6 mentioned.<br>
                    <br>
                    To record and upload your image ensure that the top left 400 pixels are sharp or
                    that the image taken is in a 400x400 resolution, taken from aproximately 6cm
                    of the fabrics surface with 4 times zoom, looking straight at the fabric with no direct shadow casted onto 
                    the surface.<br>
                    For examples on how images should look like visit https://ibug.doc.ic.ac.uk/resources/fabrics/.<br>
                    <br>
                    Operation:<br>
                    <ul>
                    <li>Use the file selector below to select a .jpg or .png (recommended) image
                    on your device.</li>
                    <li>Press the upload button.</li>
                    <li>If no errors occurred you will be shown the classification results for the
                    uploaded image in the form of a % which indicates of the identifiable fabrics
                    which image has the largest likelihood to be of a certain fabric.</li>
                    <li>In addtion to that a short summary will be provided on how you can perform a test to
                    be certain that the fabric was corretly identified.</li>
                    </ul>""")
    return render_template('index.html', prediction_text="", information_text = intro_Text, result_data="")

@APP.route('/result', methods=['POST'])
def predict_request():
    # Get file and save it
    file = request.files['filetoupload']
    #filename = secure_filename(file.filename)

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