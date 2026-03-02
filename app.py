import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for

app = Flask(__name__)

# IMPORTANT : On utilise /uploads pour correspondre au disque Render
UPLOAD_FOLDER = '/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    folders = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isdir(os.path.join(UPLOAD_FOLDER, f))]
    return render_template('index.html', folders=folders)

@app.route('/create_folder', methods=['POST'])
def create_folder():
    folder_name = request.form.get('folder_name')
    if folder_name:
        path = os.path.join(UPLOAD_FOLDER, folder_name)
        if not os.path.exists(path):
            os.makedirs(path)
    return redirect(url_for('index'))

@app.route('/folder/<name>')
def view_folder(name):
    folder_path = os.path.join(UPLOAD_FOLDER, name)
    files = os.listdir(folder_path)
    return render_template('folder.html', folder_name=name, files=files)

@app.route('/upload/<folder_name>', methods=['POST'])
def upload_file(folder_name):
    file = request.files.get('file')
    if file and file.filename != '':
        target_path = os.path.join(UPLOAD_FOLDER, folder_name)
        file.save(os.path.join(target_path, file.filename))
    return redirect(url_for('view_folder', name=folder_name))

@app.route('/download/<folder_name>/<filename>')
def download_file(folder_name, filename):
    return send_from_directory(os.path.join(UPLOAD_FOLDER, folder_name), filename)

if __name__ == '__main__':
    app.run()