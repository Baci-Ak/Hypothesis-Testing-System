import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from io import BytesIO
from user_Interface import hypothesis_System_interface

app = Flask(__name__)

app.secret_key = '0456734'  # Set the secret key for the Flask app
UPLOAD_FOLDER = 'uploads'  # Folder to store uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx', 'sas7bdat'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Load filenames in the upload folder if they exist
    filenames = os.listdir(UPLOAD_FOLDER) if os.path.exists(UPLOAD_FOLDER) else []
    return render_template('index.html', filenames=filenames)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected. Please choose a file.', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        try:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)  # Save the file to the upload folder

            # Read the file for variable options
            if filename.endswith('.sas7bdat'):
                df = pd.read_sas(file_path)
            elif filename.endswith('.xlsx') or filename.endswith('.xls'):
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)
            
            variable_options = df.columns.tolist()
            flash('File uploaded successfully.', 'success')
            return render_template('index.html', filenames=os.listdir(app.config['UPLOAD_FOLDER']), variable_options=variable_options)
        except Exception as e:
            flash(f'Error processing the file: {e}', 'error')
            return redirect(url_for('index'))
    else:
        flash('Unsupported file format. Please choose a CSV, Excel, or SAS7BDAT file.', 'error')
    return redirect(url_for('index'))

@app.route('/test', methods=['POST'])
def perform_test():
    try:
        # Retrieve data from the form
        filename = request.form['filename']
        alpha = float(request.form['alpha'])
        test_type = request.form['test_type']
        items = request.form['items']
        
        # Ensure the file exists in the upload folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            flash('The selected file does not exist. Please upload a file.', 'error')
            return redirect(url_for('index'))

        # Read the file
        if filename.endswith('.sas7bdat'):
            df = pd.read_sas(file_path)
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)
        
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
