import os
import pandas as pd
import uuid
import logging

logger = logging.getLogger(__name__)

def generate_excel(data, output_folder):
    try:
        # Generate unique filename
        filename = f"report_{uuid.uuid4().hex[:8]}.xlsx"
        excel_path = os.path.join(output_folder, filename)
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Save to Excel
        df.to_excel(excel_path, index=False, engine='openpyxl')
        logger.info(f"Excel file generated: {excel_path}")
        
        return excel_path
    except Exception as e:
        logger.error(f"Excel generation error: {str(e)}")
        raise