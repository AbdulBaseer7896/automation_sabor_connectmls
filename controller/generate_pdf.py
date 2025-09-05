from flask import request, jsonify, render_template
import base64
from datetime import datetime
from xhtml2pdf import pisa
from io import BytesIO
import uuid
from app import app
from model.DataBase_model import get_all_json


from contract_generator import RealEstateContractGenerator

# @app.route('/generate-pdf', methods=['POST'])
# def generate_pdf():
#     try:
#         # Get property data from request
#         property_data = request.get_json()
#         if not property_data:
#             return jsonify({'status': 'error', 'message': 'No property data received'}), 400

#         # Generate a unique document ID
#         document_id = str(uuid.uuid4())[:8].upper()

#         # Render the PDF template with property data
#         html = render_template(
#             'contract_template.html',
#             property_data=property_data,
#             generation_date=datetime.now().strftime('%Y-%m-%d'),
#             document_id=document_id
#         )

#         # Create PDF
#         pdf_buffer = BytesIO()
#         pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)
        
#         if pisa_status.err:
#             return jsonify({'status': 'error', 'message': 'Error generating PDF'}), 500

#         pdf_data = pdf_buffer.getvalue()
#         pdf_buffer.close()

#         # Convert to base64 for frontend
#         pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')

#         filename = f"Property_Agreement_{property_data['address'].replace(' ', '_').replace(',', '')}.pdf"

#         return jsonify({
#             'status': 'success',
#             'message': 'PDF generated successfully',
#             'pdf': pdf_base64,
#             'filename': filename
#         })

#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)}), 500




# @app.route("/generate-pdf-page")
# def generate_pdf_page():
#     try:
#         # Get all data from the properties collection
#         properties = get_all_json(collection_name="properties")
#         return render_template("generate_pdf.html", properties=properties)
#     except Exception as e:
#         return render_template("error.html", error=str(e))
    





@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        # Get property data from request
        property_data = request.get_json()
        if not property_data:
            return jsonify({'status': 'error', 'message': 'No property data received'}), 400

        # Generate a unique document ID
        document_id = str(uuid.uuid4())[:8].upper()
        property_data["document_id"] = document_id

        # Generate PDF using the new class
        pdf_generator = RealEstateContractGenerator(property_data)

        # Instead of saving to disk, write PDF into memory
        pdf_buffer = BytesIO()
        pdf_generator.generate_pdf(pdf_buffer)
        pdf_data = pdf_buffer.getvalue()
        pdf_buffer.close()

        # Convert to base64 for frontend
        pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')

        filename = f"Property_Agreement_{property_data.get('address','Property').replace(' ', '_').replace(',', '')}.pdf"

        return jsonify({
            'status': 'success',
            'message': 'PDF generated successfully',
            'pdf': pdf_base64,
            'filename': filename
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route("/generate-pdf-page")
def generate_pdf_page():
    try:
        # Get all data from the properties collection
        properties = get_all_json(collection_name="properties")
        return render_template("generate_pdf.html", properties=properties)
    except Exception as e:
        return render_template("error.html", error=str(e))