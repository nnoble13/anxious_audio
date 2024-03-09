from flask import Flask, render_template, request, redirect
import speech_recognition as sr #use googlecloud to convert audio to text
from transformers import pipeline

app = (Flask(__name__))

sentiment_pipeline = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")

@app.route('/', methods=['GET', 'POST']) #load page and render as home page, if request is post then do smth with form data
def index():
    transcript=""
    sentiment = ""
    if request.method == 'POST':
        print('Audio received')

        if 'file' not in request.files: #redirects if file does not exist
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect #returns user back to homepage if file is blank

        if file:
            recognizer = sr.Recognizer() #initialize instance if file exists
            audioFile = sr.AudioFile(file) #create object of audio file
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None) #you can use speech to text key if not None
            print(transcript)

        results = sentiment_pipeline(transcript)
        sentiment = results[0]['label']  # Assuming you want the first result's label


    return render_template('index.html', transcript=transcript, sentiment=sentiment) #render the template with the transcript text from audio file

if __name__ == '__main__':
    app.run(debug=True, threaded=True) #refresh with latest updates, threaded wont get overloaded processing multiple fiels at the same time
