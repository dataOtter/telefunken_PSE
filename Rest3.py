import flask as f
import os
from werkzeug.utils import secure_filename
#import telefunken_n3psi as t

app = f.Flask(__name__)

@app.route("/")
def main():
    """Returns the initial html page"""
    return f.render_template('index.html')

if __name__ == "__main__":
    #app.run(host='192.168.4.1')
    print("hi")
    app.run()
