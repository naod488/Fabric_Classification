import numpy as np
import os
import PIL
import PIL.Image
import tensorflow as tf
import re
import pathlib
import matplotlib.pyplot as plt
from keras.callbacks import ModelCheckpoint
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix

"""
This is a file made to provide certain functionalitiy trough functions
repeated accross the model creation files, it capabilites are.

To create training and validation splits:
    generate_ds(data_dir, batch_size, img_height, img_width)

To display some image samples from the dataset
    def display_image(train_ds)
    
To display the augmentation applied to some sample images from the dataset
    display_augmentation(train_ds, data_augmentation)

To generate a callback function variable that specifies model saving conditions and save location
    generate_callback(path, filename)

To generate the loss and accuraccy plots from the model history
    generate_plot(hist)

To generate a confusion matrix showcasing the predictions of the trained model
    generate_cm(model, val_ds, class_names)
"""

#based of https://www.tensorflow.org/tutorials/load_data/images
# creates training and validation splits
# returns the training and validation set aswell as the class names of each type
def generate_ds(data_dir, batch_size, img_height, img_width):
    img_size = (img_height, img_width)
    
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=img_size,
        batch_size=batch_size)

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=img_size,
        batch_size=batch_size)

    class_names = train_ds.class_names

    return train_ds, val_ds, class_names

#based of https://www.tensorflow.org/tutorials/load_data/images
# displays a number of image samples from the dataset
def display_image(train_ds):
    plt.figure(figsize=(10, 10))
    for images, labels in train_ds.take(1):
        for i in range(9):
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"))
            plt.title(class_names[labels[i]])
            plt.axis("off")

#based of https://keras.io/examples/vision/image_classification_from_scratch/
# displays images with augmentaition applied
def display_augmentation(train_ds, data_augmentation):
    #visualize the effect of the augmentations on a sample image
    plt.figure(figsize=(10, 10))
    for images, _ in train_ds.take(1):
        for i in range(9):
            augmented_images = data_augmentation(images)
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(augmented_images[0].numpy().astype("uint8"))
            plt.axis("off")

    return 0


from keras.callbacks import ModelCheckpoint
#based on https://towardsdatascience.com/ai-for-textiles-convolutional-neural-network-based-fabric-structure-classifier-c0db5433501d
# generates a callbackfunction that saves a model during training whenever validation accuracy improves
def generate_callback(path = "/content/drive/MyDrive/fabric_classification/", filename = "placeholder"):
    checkpoint = ModelCheckpoint(filepath = f'{path}{filename}.h5', monitor='val_accuracy', 
                             verbose=1, save_best_only=True, mode='max')

    return checkpoint


# generate the accuraccy and loss plots for model training
def generate_plot(hist):
    plt.style.use('ggplot')
    plt.plot(hist.history['loss'], label = 'loss')
    plt.plot(hist.history['val_loss'], label='val loss')
    plt.title("Loss vs Val_Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.show()

    plt.plot(hist.history['accuracy'], label = 'acc')
    plt.plot(hist.history['val_accuracy'], label='val acc')
    plt.title("acc vs Val_acc")
    plt.xlabel("Epochs")
    plt.ylabel("acc")
    plt.legend()
    plt.show()

    return 0


def generate_cm(model, val_ds, class_names):
    y_pred = model.predict(val_ds)#X
    predicted_categories = tf.argmax(y_pred, axis=1)#X
    true_categories = tf.concat([y for x, y in val_ds], axis=0)#y

    print(y_pred.shape)

    cm = confusion_matrix(true_categories, predicted_categories)
    print(cm)
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(cm)
    plt.title('Confusion matrix of the classifier')
    fig.colorbar(cax)
    ax.set_xticklabels([''] + class_names)
    ax.set_yticklabels([''] + class_names)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

    return 0

