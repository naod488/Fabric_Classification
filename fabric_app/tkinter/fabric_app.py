from tensorflow.keras.models import load_model
import tensorflow as tf
import os
import numpy as np

from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

model = load_model("a_model_Aug_V5.h5")
types = ['Cotton', 'Denim', 'Nylon', 'Polyester', 'Silk', 'Wool']


def predict(save_path = "im_1.png"):
    #based of https://www.tensorflow.org/tutorials/images/classification
    imgSize = (400, 400)
    img = tf.keras.preprocessing.image.load_img(
        save_path, target_size=imgSize)
    
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis

    print("predicting image")
    pred = model.predict(img_array)
    
    score = tf.nn.softmax(pred[0])
    result = f"This image most likely belongs to {types[np.argmax(score)]} with \n{np.round(100 * np.max(score), 2)} percent confidence."
    return result, score


def showConfidence(predictions):
    counts = 0
    values = ""
    for val in predictions[0:6]:
        calcVal = np.round(100 * val, 2)
        values += f"{types[counts]}: " 
        values += f"{np.round(100 * float(val), 2)}% \n"
        counts += 1
    return values


def open_img():
    x = openfilename()
    img = Image.open(x)
    
    img = img.resize((200, 200), Image.ANTIALIAS)
    
    #display the uploaded image
    img = ImageTk.PhotoImage(img)
    imageLabel = Label(root, image = img)
    imageLabel.image = img
    imageLabel.config(bg="black")
    imageLabel.grid(row = 2, column = 2, sticky = "ew")

    #display the calssification results
    result, predictions = predict(x)
    resultLabel = Label(root, text = result)
    resultLabel.config(bg = "white")
    resultLabel.grid(row = 3, column = 2, sticky = "ew")

    #display the confidence values for the other options
    values = showConfidence(predictions)
    valuesLabel = Label(root, text = values)
    valuesLabel.config(bg = "white")
    valuesLabel.grid(row = 4, column = 2, sticky = "ew")


def openfilename():
    filename = filedialog.askopenfilename(title ='Open')
    return filename

root = Tk()
root.title("Image Loader")
root.geometry("275x360")
root.resizable(width = False, height = False)
root.configure(bg = "white")

btn = Button(root, text ='open image', command = open_img).grid(
                                        row = 1, column = 2, padx = 100)
#open_img()
root.mainloop()
