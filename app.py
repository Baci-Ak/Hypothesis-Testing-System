
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pandas as pd
from user_Interface import hypothesis_System_interface

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '0456734'  # Set the secret key for the Flask app

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx', 'sas7bdat'}

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected. Please choose a file.', 'error')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        df = None
        if filename.endswith('.sas7bdat'):
            df = pd.read_sas(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
        if df is not None:
            variable_options = df.columns.tolist()
            filenames = os.listdir(app.config['UPLOAD_FOLDER'])
            filenames.remove(filename)  # Remove the filename from the list
            filenames.insert(0, filename)  # Insert the filename at the beginning of the list
            return render_template('index.html', success='File uploaded successfully', filenames=filenames, variable_options=variable_options)
        else:
            flash('Unsupported file format. Please choose a CSV, Excel, or SAS7BDAT file.', 'error')
    else:
        flash('Unsupported file format. Please choose a CSV, Excel, or SAS7BDAT file.', 'error')
    return redirect(url_for('index'))

@app.route('/test', methods=['POST'])
def perform_test():
    filename = request.form['filename']
    alpha = float(request.form['alpha'])
    test_type = request.form['test_type']  
    items = request.form['items']
    
    try:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if filename.endswith('.sas7bdat'):
            df = pd.read_sas(file_path)
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)
        results = hypothesis_System_interface(df, alpha, test_type, items)
        return render_template('result.html', results=results)
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/quit', methods=['GET'])
def quit():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)




















