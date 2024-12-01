import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, session
import pandas as pd
from io import BytesIO
from user_Interface import hypothesis_System_interface

app = Flask(__name__)
app.secret_key = '0456734'  # Set the secret key for the Flask app

BASE_UPLOAD_FOLDER = 'uploads'  # Base folder to store all uploaded files
app.config['UPLOAD_FOLDER'] = BASE_UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx', 'sas7bdat'}

# Ensure the base upload folder exists
if not os.path.exists(BASE_UPLOAD_FOLDER):
    os.makedirs(BASE_UPLOAD_FOLDER)

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def ensure_user_folder():
    """Ensure each user has a unique folder for their session."""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())  # Generate a unique user ID
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['user_id'])
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    session['user_folder'] = user_folder

@app.route('/')
def index():
    # Load filenames in the user's upload folder if they exist
    filenames = os.listdir(session['user_folder'])
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
            file_path = os.path.join(session['user_folder'], filename)
            file.save(file_path)  # Save the file to the user's session folder

            # Read the file for variable options
            if filename.endswith('.sas7bdat'):
                df = pd.read_sas(file_path)
            elif filename.endswith('.xlsx') or filename.endswith('.xls'):
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)
            
            variable_options = df.columns.tolist()
            flash('File uploaded successfully.', 'success')
            return render_template('index.html', filenames=os.listdir(session['user_folder']), variable_options=variable_options)
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
        
        # Ensure the file exists in the user's upload folder
        file_path = os.path.join(session['user_folder'], filename)
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
    # Use the PORT environment variable for Heroku
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)

