from flask import Flask, render_template, request, jsonify
import os
from pocketsphinx import LiveSpeech
import numpy as np
import face_recognition

app = Flask(__name__)

def authenticate_face(user_image_path, unknown_image_path):
    # Load images
    user_image = face_recognition.load_image_file(user_image_path)
    unknown_image = face_recognition.load_image_file(unknown_image_path)

    # Encode faces
    user_encoding = face_recognition.face_encodings(user_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    # Compare faces
    results = face_recognition.compare_faces([user_encoding], unknown_encoding)

    return results[0]

def authenticate_voice(new_voice_sample):
    # Replace with your actual logic for voice authentication
    # Simulate authentication with a new voice sample
    return "Authenticated" if np.random.rand() > 0.5 else "Access Denied"

# def recognize_speech(audio_path):
#     # Use pocketsphinx for offline speech recognition
#     speech = LiveSpeech(audio_file=audio_path, verbose=False)
#     recognized_text = ""

#     for phrase in speech:
#         recognized_text += str(phrase) + " "

#     return recognized_text.strip()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    user_image_path = "./static/user_image.jpg"  # Replace with actual path
    unknown_image_path = "./static/unknown_image.jpg"  # Replace with actual path

    # Simulate voice authentication (replace with actual voice recording)
    new_voice_sample = np.random.rand(16000)

    voice_authentication_result = authenticate_voice(new_voice_sample)

    # Simulate speech recognition (replace with actual audio file)
    audio_file_path = "./static/audio_file.wav"
    # speech_recognition_result = recognize_speech(audio_file_path)

    # Perform face authentication
    face_authentication_result = authenticate_face(user_image_path, unknown_image_path)

    return jsonify({
        'voice_authentication': voice_authentication_result,
        # 'speech_recognition': speech_recognition_result,
        'face_authentication': face_authentication_result
    })

if __name__ == '__main__':
    app.run(debug=True)
