from flask import Flask, render_template, request, redirect
import speech_recognition as sr
import librosa
import soundfile as sf
import tempfile
from transformers import AutoModelForAudioClassification, AutoProcessor
import torch

app = Flask(__name__)

# Load the model and processor for audio classification
model_name = "superb/hubert-large-superb-er"
model = AutoModelForAudioClassification.from_pretrained(model_name)
processor = AutoProcessor.from_pretrained(model_name)

def classify_emotion(audio_path):
    # Preprocess the audio
    audio_input = processor(audio_path, return_tensors="pt", sampling_rate=16000)
    # Perform inference
    with torch.no_grad():
        logits = model(audio_input.input_values).logits
    # Interpret the model's output
    predicted_ids = torch.argmax(logits, dim=-1)
    labels = model.config.id2label[predicted_ids[0].item()]

    return labels

@app.route('/', methods=['GET', 'POST'])
def index():
    transcript = ""
    sentiment = ""
    if request.method == 'POST':
        print('Audio received')

        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                file.save(tmp.name)
                with sr.AudioFile(tmp.name) as source:
                    data = recognizer.record(source)
                transcript = recognizer.recognize_google(data, key=None)
                print(transcript)

                # Now classify emotion using the manually loaded model
                emotion_label = classify_emotion(tmp.name)
                sentiment = "Negative vibe detected." if emotion_label == "NEG" else "Positive vibe detected."
                print(f"Predicted emotion: {emotion_label}")

    return render_template('index.html', transcript=transcript, sentiment=sentiment)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
