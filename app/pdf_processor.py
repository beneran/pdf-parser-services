import pdfplumber
import logging
import re

logger = logging.getLogger(__name__)

def extract_data_from_pdf(pdf_path):
    extracted_data = []
    logger.info(f"Processing PDF: {pdf_path}")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages):
                # Ekstrak teks
                text = page.extract_text()
                
                if not text:
                    continue
                
                # Contoh parsing - sesuaikan dengan format Anda
                student_info = parse_student_info(text)
                subjects = parse_subjects(text)
                
                for subject, grade in subjects.items():
                    extracted_data.append({
                        'student_id': student_info.get('id', ''),
                        'student_name': student_info.get('name', ''),
                        'subject': subject,
                        'grade': grade,
                        'semester': '2023/2024'  # Contoh
                    })
        
        logger.info(f"Extracted {len(extracted_data)} records from PDF")
        return extracted_data
    
    except Exception as e:
        logger.error(f"PDF processing error: {str(e)}")
        raise

def parse_student_info(text):
    # Contoh parsing - sesuaikan dengan format Anda
    student_id = re.search(r"NIS:\s*(\d+)", text)
    student_name = re.search(r"Nama:\s*([\w\s]+)", text)
    
    return {
        'id': student_id.group(1) if student_id else '',
        'name': student_name.group(1).strip() if student_name else ''
    }

def parse_subjects(text):
    # Contoh parsing - sesuaikan dengan format Anda
    subjects = {}
    lines = text.split('\n')
    
    for line in lines:
        if ':' in line and len(line.split(':')) == 2:
            subject, grade = line.split(':')
            subjects[subject.strip()] = grade.strip()
    
    return subjects