from flask import Flask, render_template, request

app = (Flask(__name__))

@app.route('/', methods=['GET', 'POST']) #load page and render as home page, if request is post then do smth with form data
def index():
    if request.method == 'POST':
        print('Audio received')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True) #refresh with latest updates, threaded wont get overloaded processing multiple fiels at the same time
