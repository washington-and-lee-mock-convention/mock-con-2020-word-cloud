import os
import logging
import tensorflow as tf

logging.basicConfig(level=logging.INFO)
CSV_PATH = os.environ.get('CSV_PATH', '.')


class SentimentModel():

    def __init__(self, training_set, testing_set):
        self.training_set = training_set
        self.testing_set = testing_set
        self.model = self.__setup_model__()

    def __setup_model__(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(20000, 64),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(3)
        ])

        model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])

        return model

    def __train__(self):
        history = self.model.fit(
            self.training_set, epochs=10,
            validation_data=self.testing_set,
            validation_steps=30
        )

    def __call__(self):
        self.__train__()


def import_data_from_csv():
    pass


if __name__ == '__main__':
    logging.info('Setting up Sentiment Analysis Model...')
    model = SentimentModel([],[])

    logging.info('Training Sentiment Analysis Model...')
    model()