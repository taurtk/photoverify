from flask import Flask, render_template, request, jsonify
import os
import base64
from PIL import Image
from io import BytesIO
import face_recognition

app = Flask(__name__)

# Load the known face encoding (replace with the path to the known face image)
known_image_path = "./static/known_image.jpg"

if os.path.exists(known_image_path):
    known_image = face_recognition.load_image_file(known_image_path)
    known_encoding = face_recognition.face_encodings(known_image)[0]
else:
    known_encoding = None
    print(f"Known image not found at: {known_image_path}")

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/save_photo', methods=['POST'])
def save_photo():
    photo_data = request.json.get('photo', '')

    # Convert base64 photo data to image
    photo_binary = base64.b64decode(photo_data.split(",")[1])
    image = Image.open(BytesIO(photo_binary))

    # Save the image to the static folder
    image_path = "./static/captured_photo.jpg"
    image.save(image_path)

    return jsonify({'status': 'success'})

@app.route('/verify_photo', methods=['POST'])
def verify_photo():
    if known_encoding is None:
        return jsonify({'result': 'Error: Known image not found'})

    captured_image_path = "./static/captured_photo.jpg"
    captured_image = face_recognition.load_image_file(captured_image_path)

    # Encode the captured face
    captured_encoding = face_recognition.face_encodings(captured_image)

    if not captured_encoding:
        return jsonify({'result': 'Error: No face detected in the captured photo'})

    # Compare faces
    results = face_recognition.compare_faces([known_encoding], captured_encoding[0])

    return jsonify({'result': 'Authenticated' if results[0] else 'Access Denied'})

if __name__ == '__main__':
    app.run(debug=True)
