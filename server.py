import os
import hashlib
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
app.secret_key = '2nd'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

USERNAME = "zt"
PASSWORD = "123"

files = []

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', files=files)

@app.route('/statistics')
@login_required
def statistics():

    total_logs = len(files)
    unique_ips = len(set(file['ip'] for file in files))

    from datetime import datetime, timedelta
    days = [(datetime.now() - timedelta(days=i)).strftime('%d.%m') for i in range(6, -1, -1)]
    uploads_per_day = {day: 0 for day in days}
    for file in files:
        file_date = file.get('date')
        if file_date in uploads_per_day:
            uploads_per_day[file_date] += 1
    chart_data = {
        'labels': list(uploads_per_day.keys()),
        'data': list(uploads_per_day.values())
    }

    return render_template('statistics.html',
                         total_logs=total_logs,
                         unique_ips=unique_ips,
                         chart_data=chart_data)

@app.route('/logs')
@login_required
def logs():
    return render_template('logs.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return '', 400

    if file:

        filename = secure_filename(file.filename)
        file_id = hashlib.md5(filename.encode()).hexdigest()
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_id)
        file.save(file_path)

        file_size = os.path.getsize(file_path)
        size_str = f"{file_size / 1024:.1f} kB" if file_size < 1024*1024 else f"{file_size / (1024*1024):.1f} MB"

        ip_address = request.remote_addr

        from datetime import datetime
        file_date = datetime.now().strftime('%d.%m')

        files.append({
            'id': file_id,
            'name': filename,
            'size': size_str,
            'ip': ip_address,
            'date': file_date
        })

        return 'File uploaded successfully', 200
@app.route('/download/<file_id>')
@login_required
def download_file(file_id):

    file_data = next((f for f in files if f['id'] == file_id), None)

    if file_data:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_id)
        return send_file(file_path, as_attachment=True, download_name=file_data['name'])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=1111, debug=True)
