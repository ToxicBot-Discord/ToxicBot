from keras.models import model_from_json
from keras.preprocessing.sequence import pad_sequences
from keras.losses import BinaryCrossentropy
from keras.metrics import AUC
from keras.optimizers import Adam


import logging
import os
import pickle

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # Tensorflow logging set to FATAL to ensure unnecessary logging
logging.getLogger("tensorflow").setLevel(logging.FATAL)

# Files present in the dump folder
EMBEDDING_DUMP = "ToxicBot_GloVeEmbedding.json"
TOKENIZER_DUMP = "ToxicBot_Tokenizer.pickle"
WEIGHT_DUMP = "ToxicBot_Weights.h5"

dump_folder = os.path.join(os.getcwd(), "dump")

# Import the saved files into the program
json_file = open(os.path.join(dump_folder, EMBEDDING_DUMP), "r")
loaded_model_json = json_file.read()
json_file.close()
MODEL = model_from_json(loaded_model_json)
MODEL.load_weights(os.path.join(dump_folder, WEIGHT_DUMP))

tokenizer_pickle = open(os.path.join(dump_folder, TOKENIZER_DUMP), "rb")
TOKENIZER = pickle.load(tokenizer_pickle)
tokenizer_pickle.close()


def predict_toxicity(message):
    prediction = classify(message)
    # If probability is more than 0.5 then predict it as Toxic
    response = 1 if prediction >= 0.5 else 0
    return response


def classify(message):
    # Tokenize the message and pad it to a size of 250
    sequence = TOKENIZER.texts_to_sequences([message])
    sequence = pad_sequences(sequence, maxlen=250)

    MODEL.compile(loss=BinaryCrossentropy(), optimizer=Adam(), metrics=[AUC()])
    prediction = MODEL.predict(sequence)

    return prediction[0]


if __name__ == "__main__":
    print(predict_toxicity("Hello, how are you ?"))
