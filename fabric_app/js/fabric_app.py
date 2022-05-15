from tensorflow.keras.models import load_model
import tensorflow as tf
import os
import numpy as np
import sys
from PIL import ImageTk, Image
from tkinter import filedialog

model = load_model("a_model_Aug_V5.h5")
types = ['Cotton', 'Denim', 'Nylon', 'Polyester', 'Silk', 'Wool']


def predict(save_path):
    try:
        #based of https://www.tensorflow.org/tutorials/images/classification
        imgSize = (400, 400)
        img = tf.keras.preprocessing.image.load_img(
            save_path, target_size=imgSize)
        
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create batch axis

        #print("predicting image")
        pred = model.predict(img_array)
        
        score = tf.nn.softmax(pred[0])
        result = f"This image most likely belongs to {types[np.argmax(score)]} with \n{np.round(100 * np.max(score), 2)} percent confidence."
        return result, score
    
    except Exception as e:
        return "Image invalid: ", "Image invalid: "


def showConfidence(predictions):
    try:
        counts = 0
        values = ""
        for val in predictions[0:6]:
            calcVal = np.round(100 * val, 2)
            values += f"{types[counts]}: " 
            values += f"{np.round(100 * float(val), 2)}% \n"
            counts += 1
        return values

    except Exception as e:
        return "Image invalid: "


def open_img(name = "im_1.png"):
    try:
        #display the calssification results
        result, predictions = predict(name)

        #display the confidence values for the other options
        values = showConfidence(predictions)
        
        #return result, values, predictions
        return result
    except Exception as e:
        return "Image invalid: "

print(open_img(sys.argv[1]))