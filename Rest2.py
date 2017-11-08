import flask as f

app = f.Flask(__name__)

@app.route("/")
def main():
    """Returns the initial html page"""
    print("hi2")
    return f.render_template('index.html')

if __name__ == "__main__":
    #app.run(host='192.168.4.1')
    print("hi")
    app.run()
