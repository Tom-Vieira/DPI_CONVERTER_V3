"""
app.py

Author: Cleilton Vieira
Email: cleilton7700@gmail.com
Date: 2024-06-16
Description: Aplicação Flask para alterar o DPI de imagens e permitir download.
"""


from flask import Flask, request, render_template, send_from_directory, redirect, url_for
from PIL import Image
import os
import zipfile
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('file')
        dpi = int(request.form['dpi'])

        if len(files) == 0 or len(files) > 10:
            return "Você deve selecionar entre 1 e 10 arquivos."

        modified_files = []
        for file in files:
            if file.filename == '':
                return 'Arquivo não selecionado'
            if file:
                image = Image.open(file)
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                image.save(file_path, dpi=(dpi, dpi))
                modified_files.append(file.filename)

        # Criação de um arquivo zip para download
        zip_filename = f'modified_images_{datetime.now().strftime("%Y%m%d%H%M%S")}.zip'
        zip_path = os.path.join(UPLOAD_FOLDER, zip_filename)
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for filename in modified_files:
                zipf.write(os.path.join(UPLOAD_FOLDER, filename), filename)

        return redirect(url_for('download_file', filename=zip_filename))

    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)