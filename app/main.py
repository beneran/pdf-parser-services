import os
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from app.pdf_processor import extract_data_from_pdf
from app.database import save_to_database
from app.utils import generate_excel
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Konfigurasi dari environment variables
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['DATABASE'] = os.getenv('DB_PATH', 'reports.db')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Pastikan folder upload ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(pdf_path)

        try:
            # Proses PDF
            extracted_data = extract_data_from_pdf(pdf_path)
            
            if not extracted_data:
                return jsonify({'error': 'No data extracted from PDF'}), 400
            
            # Simpan ke database
            save_to_database(extracted_data, app.config['DATABASE'])
            
            # Generate Excel
            excel_path = generate_excel(extracted_data, app.config['UPLOAD_FOLDER'])
            
            return send_file(
                excel_path,
                as_attachment=True,
                download_name='report_data.xlsx',
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        
        except Exception as e:
            app.logger.error(f'Error processing file: {str(e)}')
            return jsonify({'error': str(e)}), 500
        
        finally:
            # Bersihkan file sementara
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
    
    return jsonify({'error': 'Invalid file type. Only PDF allowed'}), 400

if __name__ == '__main__':
    # Buat folder jika belum ada
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.dirname(app.config['DATABASE']), exist_ok=True)
    
    # Inisialisasi database
    from app.database import init_db
    init_db(app.config['DATABASE'])

    app.run(host='0.0.0.0', port=5000)