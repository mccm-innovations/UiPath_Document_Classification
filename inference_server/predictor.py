import numpy as np
from PIL import Image
import flask
from pdf2image import convert_from_bytes
import tensorflow as tf
from keras.models import load_model
import json
import io

IMAGE_SIZE = 224
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def get_file_extension(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower()


idx2label = {0: 'driving_licence',
             1: 'id_card_2',
             2: 'id_card_3',
             3: 'invoice',
             4: 'passport'}


# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.

class ClassificationService(object):
    model = None
    graph = None

    @classmethod
    def get_model(cls):
        if cls.model is None:
            cls.model = load_model('model.hdf5')
            cls.graph = tf.get_default_graph()
        return cls.model

    @classmethod
    def get_graph(cls):
        if cls.graph is None:
            cls.get_model()
        return cls.graph

    @classmethod
    def predict(cls, image):
        with cls.get_graph().as_default():
            predictions = np.squeeze(cls.get_model().predict(image))
            confidences = {}
            for idx, prediction in enumerate(predictions):
                confidences[idx2label[idx]] = '{:.3f}'.format(prediction)
            pred = {'class': idx2label[np.argmax(predictions)], 'confidence': str(np.max(predictions))}
            result = {
                'prediction': pred,
                'confidences': confidences
            }
            json_result = json.dumps(result)
            return json_result


# The flask app for serving predictions
app = flask.Flask(__name__)


@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = ClassificationService.get_model() is not None
    status = 200 if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')


@app.route('/document_classification', methods=['POST'])
def document_classification():
    if flask.request.files.get('file'):
        file = flask.request.files['file']
        file_extension = get_file_extension(file.filename)
        if file and file_extension in ALLOWED_EXTENSIONS:
            if file_extension == 'pdf':
                pdf = file.read()
                images = convert_from_bytes(pdf, fmt='jpg')
                image = images[0]
            else:
                image = Image.open(io.BytesIO(file.read()))
                if file_extension == 'png' or file_extension == 'gif':
                    image = image.convert('RGB')
            image = image.resize((IMAGE_SIZE, IMAGE_SIZE), resample=Image.NEAREST)
            image = np.array(image).astype(np.float32)
            image = image / 255
            image = np.expand_dims(image, axis=0)
            classification_service = ClassificationService()
            js = classification_service.predict(image)
            return flask.Response(response=js, status=200, mimetype='application/json')
        else:
            return flask.Response(response='File extension not allowed. Allowed:[pdf, png, jpg, jpeg, gif]',
                                  status=415, mimetype='text/plain')
    else:
        return flask.Response(response='Parameter [file] is required.', status=415, mimetype='text/plain')
