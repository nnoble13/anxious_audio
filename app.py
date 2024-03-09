from flask import Flask, render_template

app = (Flask(__name__))

@app.route('/', methods=['GET'])
def index():
    return 'hello bros'

if __name__ == '__main__':
    app.run(debug=True, threaded=True) #refresh with latest updates, threaded wont get overloaded processing multiple fiels at the same time
