from __future__ import division, print_function

import numpy as np


from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image






def model_predict(img_path):
    # Model saved with Keras model.save()
    MODEL_PATH = 'effnet_liver.h5'

    # Load your trained model
    model = load_model(MODEL_PATH)

    img = image.load_img(img_path, target_size=(150, 150))
    x=np.asarray(img)


    x = np.expand_dims(x, axis=0)

    preds = model.predict(x)
    print(preds)
    pred = np.argmax(preds, axis=1)
    print(pred)
    if pred == 0:
        pred = "Bile Duct"
    elif pred == 1:
        pred = "Fibromellar Carcinoma"
    elif pred == 2:
        pred = "Hepatocellular Carcinoma(HCC)"
    elif pred == 3:
        pred = "Hepatoblastoma"
    elif pred == 4:
        pred = "Normal"
    return pred