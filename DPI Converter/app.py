from flask import Flask, request, render_template, redirect, url_for, flash, send_file, send_from_directory
from PIL import Image
import os
import zipfile
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.static_url_path = '/static'  # Define o caminho URL para arquivos estáticos

UPLOAD_FOLDER = 'static/uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Função para limpar arquivos antigos
def clean_old_files():
    now = datetime.now()
    cutoff = now - timedelta(days=1)
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_time < cutoff:
                os.remove(file_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('file')
        dpi = request.form.get('dpi')

        if not dpi or not dpi.isdigit():
            flash('DPI inválido.')
            return redirect(url_for('index'))

        dpi = int(dpi)

        if len(files) == 0 or len(files) > 100:
            flash('Você deve selecionar entre 1 e 100 arquivos.')
            return redirect(url_for('index'))

        # Lista para armazenar caminhos relativos das imagens processadas
        processed_images = []

        try:
            for file in files:
                if file.filename == '':
                    flash('Arquivo não selecionado.')
                    return redirect(url_for('index'))
                if file:
                    try:
                        image = Image.open(file)
                        # Obtém o diretório de origem do arquivo
                        source_folder = os.path.dirname(file.filename)
                        # Constrói o caminho de salvamento na pasta de origem
                        file_path = os.path.join(source_folder, file.filename)
                        # Garantir que o caminho de salvamento seja seguro e válido
                        safe_file_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, file_path))
                        # Salva o arquivo modificado
                        image.save(safe_file_path, dpi=(dpi, dpi))
                        processed_images.append(file_path)  # Armazena o caminho relativo da imagem processada
                        flash(f'Arquivo modificado salvo em: {safe_file_path}')
                    except Exception as e:
                        flash(f'Erro ao processar o arquivo {file.filename}: {e}')
                        continue

            clean_old_files()  # Limpa arquivos antigos

            if len(processed_images) > 0:
                flash('DPI aplicado com sucesso.')
                return render_template('index.html', processed_images=processed_images)
            else:
                flash('Nenhum arquivo foi processado.')
                return redirect(url_for('index'))

        except Exception as e:
            flash(f'Ocorreu um erro: {e}')
            return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/download_all')
def download_all():
    try:
        files_to_zip = os.listdir(UPLOAD_FOLDER)
        zip_filename = f'modified_images_{datetime.now().strftime("%Y%m%d%H%M%S")}.zip'
        zip_path = os.path.join(UPLOAD_FOLDER, zip_filename)

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for filename in files_to_zip:
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                zipf.write(file_path, filename)
        
        return send_file(zip_path, as_attachment=True)

    except Exception as e:
        flash(f'Ocorreu um erro ao criar o arquivo ZIP: {e}')
        return redirect(url_for('index'))

@app.route('/download/<path:filename>')
def download_image(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except Exception as e:
        flash(f'Ocorreu um erro ao baixar o arquivo {filename}: {e}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
