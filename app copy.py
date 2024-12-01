
import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
from user_Interface import hypothesis_System_interface

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        variable_options = df.columns.tolist()
        return render_template('index.html', success='File uploaded successfully', filenames=os.listdir(app.config['UPLOAD_FOLDER']), variable_options=variable_options)

@app.route('/test', methods=['POST'])
def perform_test():
    filename = request.form['filename']
    alpha = float(request.form['alpha'])
    test_type = request.form['test_type']  # Added this line
    items = request.form['items']  # Added this line
    df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    results = hypothesis_System_interface(df, alpha, test_type, items)  # Updated this line
    return render_template('result.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)



