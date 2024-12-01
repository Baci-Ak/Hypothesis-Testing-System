import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from io import BytesIO
from user_Interface import hypothesis_System_interface

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = '0456734'  # Set the secret key for the Flask app
UPLOAD_FOLDER = 'uploads'  # Folder to store uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx', 'sas7bdat'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    try:
        # Load filenames in the upload folder if they exist
        filenames = os.listdir(UPLOAD_FOLDER) if os.path.exists(UPLOAD_FOLDER) else []
        logger.debug(f"Available files: {filenames}")
        return render_template('index.html', filenames=filenames)
    except Exception as e:
        logger.error(f"Error loading index page: {e}")
        flash(f"Error loading index page: {e}", "error")
        return render_template('index.html', filenames=[])

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(url_for('index'))

        file = request.files['file']
        if file.filename == '':
            flash('No file selected. Please choose a file.', 'error')
            return redirect(url_for('index'))

        if file and allowed_file(file.filename):
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
            logger.debug(f"Uploaded file: {filename}, Columns: {variable_options}")
            flash('File uploaded successfully.', 'success')
            return render_template('index.html', filenames=os.listdir(app.config['UPLOAD_FOLDER']), variable_options=variable_options)
        else:
            flash('Unsupported file format. Please choose a CSV, Excel, or SAS7BDAT file.', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        flash(f"Error processing the file: {e}", 'error')
        return redirect(url_for('index'))

@app.route('/test', methods=['POST'])
def perform_test():
    try:
        # Retrieve data from the form
        filename = request.form['filename']
        alpha = float(request.form['alpha'])
        test_type = request.form['test_type']
        items = request.form['items']

        logger.debug(f"Received test request: filename={filename}, alpha={alpha}, test_type={test_type}, items={items}")

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

        logger.debug(f"File loaded successfully: {filename}, Shape: {df.shape}")

        # Perform hypothesis testing
        results = hypothesis_System_interface(df, alpha, test_type, items)

        # Check if there is an error in the results
        if 'error' in results:
            flash(results['error'], 'error')
            return redirect(url_for('index'))

        logger.debug(f"Test results: {results}")
        return render_template('result.html', results=results)
    except Exception as e:
        logger.error(f"Error performing test: {e}")
        return render_template('result.html', results={'error': f"An error occurred: {e}"})

@app.route('/quit', methods=['GET'])
def quit():
    return redirect('/')

if __name__ == '__main__':
    # Use the PORT environment variable for Heroku
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

