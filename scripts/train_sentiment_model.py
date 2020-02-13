import os
import math
import logging
import tensorflow as tf
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO)
CSV_PATH = os.environ.get('CSV_PATH', '.')


class SentimentModel():

    def __init__(self, x_train, y_train, x_test, y_test):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.model = self.__setup_model__()

    def __setup_model__(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(20000, 64),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
            tf.keras.layers.Dense(3, activation='sigmoid')
        ])

        model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])

        model.summary()

        return model

    def __train__(self):
        history = self.model.fit(
            self.x_train, self.y_train,
            epochs=10,
            validation_data=(self.x_test, self.y_test),
            validation_steps=30
        )

    def __call__(self):
        self.__train__()


def import_data_from_csv():
    df = pd.read_csv(CSV_PATH + '/corpus.csv', sep=',', header=None)
    array = df.values
    token_strings = np.array([val[0] for val in array])
    labels = np.array([val[1:] for val in array])
    return (
        token_strings[:math.ceil(len(token_strings)*0.75)],
        labels[:math.ceil(len(labels)*0.75)]
    ), (
        token_strings[math.floor(len(token_strings)*0.75):],
        labels[math.floor(len(labels)*0.75):]
    )


if __name__ == '__main__':
    logging.info('Importing data from csv...')
    (x_train, y_train), (x_test, y_test) = import_data_from_csv()

    logging.info('Setting up Sentiment Analysis Model...')
    model = SentimentModel(x_train, y_train, x_test, y_test)

    logging.info('Training Sentiment Analysis Model...')
    model()
