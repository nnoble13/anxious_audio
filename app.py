from flask import Flask, render_template, request, redirect
import speech_recognition as sr #use googlecloud to convert audio to text


app = (Flask(__name__))

@app.route('/', methods=['GET', 'POST']) #load page and render as home page, if request is post then do smth with form data
def index():
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
            text = recognizer.recognize_google(data, key=None) #you can use speech to text key if not None
            print(text)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True) #refresh with latest updates, threaded wont get overloaded processing multiple fiels at the same time
