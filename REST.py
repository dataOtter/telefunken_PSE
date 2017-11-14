import flask as f
import os
from werkzeug.utils import secure_filename
import telefunken_run as t

UPLOAD_FOLDER = 'C:\\Users\\Maisha\\Dropbox\\MB_dev\\telefunken_PSE\\testfiles\\downloaded'
ALLOWED_EXTENSIONS = ['csv']

app = f.Flask(__name__)
app.secret_key = "It's secret, duh"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit for file upload


@app.route("/")
def main():
    """Returns the initial html page"""
    return f.render_template('index.html')


@app.route("/formulas")
def formulas():
    """Returns the formulas html page"""
    return f.render_template('formulas.html')


@app.route("/about")
def about():
    """Returns the about html page"""
    return f.render_template('about.html')


@app.route("/show_results", methods=["POST"])
def show_result():
    """get file and do formula operations; return various results/numbers"""
    if f.request.method == 'POST':
        # check if the post request has the file part
        if 'rdsat' not in f.request.files:  # this should never hit as I check for it in jQuery
            return f.jsonify({"result": 'No file submitted'})

        file = f.request.files['rdsat']
        name = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], name)

        if name == ''or not allowed_file(name):
            return f.jsonify({"result": "Please upload a CSV file"})

        try:
            file.save(filepath)
        except Exception as e:
            return f.jsonify({"result": str(e) + "\nError saving file"})

        formulas_selected = f.request.form['funcs_selected'].split(',')

        result = t.run_selected_formulas(filepath, formulas_selected)

    for entry in result:
        print(result[entry])

    return f.jsonify({"result": result, "filename": name})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    #app.run(host='192.168.4.1')
    print("hi")
    app.run()
