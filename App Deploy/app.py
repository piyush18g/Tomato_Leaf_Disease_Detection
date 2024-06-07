from __future__ import division, print_function
import os
import numpy as np
import tensorflow as tf
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename

# Define a flask app
app = Flask(__name__)

# Suppress TensorFlow GPU memory allocation warnings
config = ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.5
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

# Model saved with Keras model.save()
MODEL_PATH = 'tomato_leaf_model.h5'

# Load your trained model
model = load_model(MODEL_PATH)

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = x / 255 #normalizing pixel value of image
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x)
    preds = np.argmax(preds, axis=1)
    classes = ["Tomato__Bacterial_spot", "Tomato__Early_blight", "Tomato__Late_blight", "Tomato__Leaf_Mold",
               "Tomato__Septoria_leaf_spot", "Tomato__Spider_mites Two-spotted_spider_mite",
               "Tomato__Target_Spot","Tomato__Tomato_Yellow_Leaf_Curl_Virus" , "Tomato__Tomato_mosaic_virus", "Tomato__healthy" ]
    result = classes[preds[0]]
    return result

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']
        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        # Make prediction
        preds = model_predict(file_path, model)
        return preds
    return None

if __name__ == '__main__':
    app.run(port=5001, debug=True)