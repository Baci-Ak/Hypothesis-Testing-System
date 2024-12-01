import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import pandas as pd
from user_Interface import hypothesis_System_interface

app = Flask(__name__)
app.secret_key = '0456734'

BASE_UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = BASE_UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx', 'sas7bdat'}

if not os.path.exists(BASE_UPLOAD_FOLDER):
    os.makedirs(BASE_UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def ensure_user_folder():
    """Ensure each user has a unique folder for their session."""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['user_id'])
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    session['user_folder'] = user_folder

@app.route('/')
def index():
    filenames = os.listdir(session['user_folder'])
    variable_options = session.get('variable_options', [])
    return render_template('index.html', filenames=filenames, variable_options=variable_options)

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
            file.save(file_path)

            if filename.endswith('.sas7bdat'):
                df = pd.read_sas(file_path)
            elif filename.endswith('.xlsx') or filename.endswith('.xls'):
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)
            
            variable_options = df.columns.tolist()
            session['variable_options'] = variable_options
            flash('File uploaded successfully.', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error processing the file: {e}', 'error')
            return redirect(url_for('index'))
    else:
        flash('Unsupported file format. Please choose a CSV, Excel, or SAS7BDAT file.', 'error')
    return redirect(url_for('index'))

@app.route('/get_columns', methods=['GET'])
def get_columns():
    filename = request.args.get('file')
    file_path = os.path.join(session['user_folder'], filename)

    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404

    try:
        if filename.endswith('.sas7bdat'):
            df = pd.read_sas(file_path)
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)

        return jsonify({'columns': df.columns.tolist()})
    except Exception as e:
        return jsonify({'error': f'Error reading file: {e}'}), 500

@app.route('/test', methods=['POST'])
def perform_test():
    try:
        filename = request.form['filename']
        alpha = float(request.form['alpha'])
        test_type = request.form['test_type']
        items = request.form['items']
        
        file_path = os.path.join(session['user_folder'], filename)
        if not os.path.exists(file_path):
            flash('The selected file does not exist. Please upload a file.', 'error')
            return redirect(url_for('index'))

        if filename.endswith('.sas7bdat'):
            df = pd.read_sas(file_path)
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)
        
        items_list = [item.strip() for item in items.split(',')]
        
        if test_type == "two-tailed" and len(items_list) != 2:
            flash('Two variables are required for a two-tailed test.', 'error')
            return redirect(url_for('index'))
        
        for item in items_list:
            if item not in df.columns:
                flash(f'Column "{item}" does not exist in the selected file.', 'error')
                return redirect(url_for('index'))
        
        results = hypothesis_System_interface(df, alpha, test_type, items)
        return render_template('result.html', results=results)
    except ValueError as ve:
        flash(f'Invalid input: {ve}', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'An unexpected error occurred: {e}', 'error')
        return redirect(url_for('index'))

@app.route('/quit', methods=['GET'])
def quit():
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
