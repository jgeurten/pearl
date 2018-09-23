# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 20:10:32 2018

@author: Jordan
"""

import tensorflow as tf
from PIL import Image

hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))

#Load the NIST dataset from google (handdrawn numbers)
#mnist = tf.keras.datasets.mnist
#(x_train, y_train), (x_test, y_test) = mnist.load_data()
#x_train = x_train/255.0
#x_test = x_test/255.0
#
#model = tf.keras.models.Sequential([
#  tf.keras.layers.Flatten(),
#  tf.keras.layers.Dense(512, activation=tf.nn.relu),
#  tf.keras.layers.Dropout(0.2),
#  tf.keras.layers.Dense(10, activation=tf.nn.softmax)
#])
#
#model.compile(optimizer='adam',
#              loss='sparse_categorical_crossentropy',
#              metrics=['accuracy'])
#model.fit(x_train, y_train, epochs=5)
#model.evaluate(x_test, y_test)

for i in range(0, 3):
    img = Image.open(x_test[i])
    img.show()