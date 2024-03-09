from flask import Flask, render_template, request, redirect
import speech_recognition as sr
import librosa
import soundfile as sf
import tempfile
from transformers import pipeline

app = Flask(__name__)

# Initialize HuBERT pipeline for audio classification
hubert_pipeline = pipeline("audio-classification", model="superb/hubert-large-superb-er")

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
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                file.save(tmp.name)
                with sr.AudioFile(tmp.name) as source:
                    data = recognizer.record(source)
                transcript = recognizer.recognize_google(data, key=None)
                print(transcript)

                # Process audio for HuBERT
                audio, sr_librosa = librosa.load(tmp.name, sr=None)
                audio_resampled = librosa.resample(audio, orig_sr=sr_librosa, target_sr=16000)
                # Save resampled audio to a new temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_resampled:
                    sf.write(tmp_resampled, audio_resampled, 16000)
                    results = hubert_pipeline(model_input=tmp_resampled.name)

            mood = results[0]['label']
            sentiment = "Negative vibe detected." if mood == "NEG" else "Positive vibe detected."

    return render_template('index.html', transcript=transcript, sentiment=sentiment)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
