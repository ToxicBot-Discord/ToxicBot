from keras.preprocessing.text import Tokenizer
from keras.models import model_from_json
from keras.preprocessing.sequence import pad_sequences
from keras.losses import BinaryCrossentropy
from keras.metrics import AUC
from keras.optimizers import Adam

import logging
import os
import pickle

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # FATAL
logging.getLogger('tensorflow').setLevel(logging.FATAL)

EMBEDDING_DUMP = 'glove_embedding.json'
TOKENIZER_DUMP = 'tokenizer.pickle'
WEIGHT_DUMP = 'weights.h5'

dump_folder = os.path.join(os.getcwd(), 'dump')

json_file = open(os.path.join(dump_folder, EMBEDDING_DUMP), 'r')
loaded_model_json = json_file.read()
json_file.close()
MODEL = model_from_json(loaded_model_json)
MODEL.load_weights(os.path.join(dump_folder, WEIGHT_DUMP))

tokenizer_pickle = open(os.path.join(dump_folder, TOKENIZER_DUMP), 'rb')
TOKENIZER = pickle.load(tokenizer_pickle)
tokenizer_pickle.close()


def classify(message):
    sequence = TOKENIZER.texts_to_sequences([message])
    sequence = pad_sequences(sequence, maxlen=250)

    MODEL.compile(loss=BinaryCrossentropy(), optimizer=Adam(), metrics=[AUC()])
    prediction = MODEL.predict(sequence)

    print(prediction)


if __name__ == '__main__':
    classify("Hello, how are you ?")
