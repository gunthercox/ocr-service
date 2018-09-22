from flask import Flask, request, jsonify
from PIL import Image
import pytesseract

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    if 'image' not in request.files:
        return jsonify(
            error={
                'image': 'This field is required.'
            }
        ), 400

    image = Image.open(request.files['image'])

    image_text = pytesseract.image_to_string(
        image,
        lang='eng'
    )

    return jsonify({
        'text': image_text
    })
