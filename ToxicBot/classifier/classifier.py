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

EMBEDDING_DUMP = 'ToxicBot_GloVeEmbedding.json'
TOKENIZER_DUMP = 'ToxicBot_Tokenizer.pickle'
WEIGHT_DUMP = 'ToxicBot_Weights.h5'

dump_folder = os.path.join(os.getcwd(), 'dump')

json_file = open(os.path.join(dump_folder, EMBEDDING_DUMP), 'r')
loaded_model_json = json_file.read()
json_file.close()
MODEL = model_from_json(loaded_model_json)
MODEL.load_weights(os.path.join(dump_folder, WEIGHT_DUMP))

tokenizer_pickle = open(os.path.join(dump_folder, TOKENIZER_DUMP), 'rb')
TOKENIZER = pickle.load(tokenizer_pickle)
tokenizer_pickle.close()


def predict_toxicity(message):
    prediction = classify(message)
    response = [1 if x >= 0.5 else 0 for x in prediction]
    return response


def classify(message):
    sequence = TOKENIZER.texts_to_sequences([message])
    sequence = pad_sequences(sequence, maxlen=250)

    MODEL.compile(loss=BinaryCrossentropy(), optimizer=Adam(), metrics=[AUC()])
    prediction = MODEL.predict(sequence)

    return prediction[0]


if __name__ == '__main__':
    print(predict_toxicity("Hello, how are you ?"))
