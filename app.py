import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from io import BytesIO
from user_Interface import hypothesis_System_interface

app = Flask(__name__)

app.secret_key = '0456734'  # Set the secret key for the Flask app

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
        try:
            # Read the file directly from memory
            if file.filename.endswith('.sas7bdat'):
                df = pd.read_sas(BytesIO(file.read()))
            elif file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
                df = pd.read_excel(file)
            else:
                df = pd.read_csv(file)
            
            variable_options = df.columns.tolist()
            return render_template('index.html', success='File uploaded successfully', variable_options=variable_options, filename=file.filename)
        except Exception as e:
            flash(f'Error processing the file: {e}', 'error')
            return redirect(url_for('index'))
    else:
        flash('Unsupported file format. Please choose a CSV, Excel, or SAS7BDAT file.', 'error')
    return redirect(url_for('index'))

@app.route('/test', methods=['POST'])
def perform_test():
    try:
        # Retrieve data sent from the form
        file = request.files['file']
        alpha = float(request.form['alpha'])
        test_type = request.form['test_type']
        items = request.form['items']
        
        # Process the uploaded file
        if file and allowed_file(file.filename):
            if file.filename.endswith('.sas7bdat'):
                df = pd.read_sas(BytesIO(file.read()))
            elif file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
                df = pd.read_excel(file)
            else:
                df = pd.read_csv(file)
        else:
            flash('Invalid or missing file. Please upload a valid file.', 'error')
            return redirect(url_for('index'))
        
        # Perform hypothesis testing
        results = hypothesis_System_interface(df, alpha, test_type, items)
        return render_template('result.html', results=results)
    except Exception as e:
        flash(f'An error occurred: {e}', 'error')
        return redirect(url_for('index'))

@app.route('/quit', methods=['GET'])
def quit():
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
