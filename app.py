from flask import Flask, request, jsonify, send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import reportlab.rl_config  # Explicitly import the rl_config
from PyPDF2 import PdfReader, PdfWriter
import io
import os

app = Flask(__name__)

@app.route('/generate_certificate', methods=['POST'])
def generate_certificate():
    try:
        # Parse JSON data from the request
        data = request.json
        student = data.get('name')
        college = data.get('college')
        course = data.get('course', 'General Course')  # Default course
        date = data.get('date', '13 - 12 - 2024')      # Default date

        if not student or not college:
            return jsonify({"error": "Name and college are required fields"}), 400

        # Set up a canvas for the certificate
        packet = io.BytesIO()
        width, height = letter
        c = canvas.Canvas(packet, pagesize=(width * 2, height * 2))

        # Register fonts
        reportlab.rl_config.warnOnMissingFontGlyphs = 0
        pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
        pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
        pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))

        # Add text to the certificate
        try:
            c.setFillColorRGB(139 / 255, 119 / 255, 40 / 255)  # Gold color for the name
            c.setFont('VeraBd', 50)
            c.drawCentredString(422, 310, student)

            c.setFont('Vera', 25)
            c.drawCentredString(422, 260, college)

            c.setFont('Vera', 25)
            c.drawCentredString(422, 210, course)

            c.setFillColorRGB(1 / 255, 1 / 255, 1 / 255)  # Black color for the date
            c.setFont('VeraBI', 16)
            c.drawCentredString(578, 77, date)

            c.save()
        except Exception as e:
            return jsonify({"error": f"Error while drawing text on canvas: {str(e)}"}), 500

        # Merge the generated text with the certificate template
        try:
            packet.seek(0)
            new_pdf = PdfReader(packet)
            existing_pdf = PdfReader(open("Input/certificate_template.pdf", "rb"))
            page = existing_pdf.pages[0]
            page.merge_page(new_pdf.pages[0])

            # Save the final certificate
            output_dir = "Certificates"
            os.makedirs(output_dir, exist_ok=True)
            file_name = f"{student.replace(' ', '_')}_certificate.pdf"
            output_path = os.path.join(output_dir, file_name)
            with open(output_path, "wb") as outputStream:
                output = PdfWriter()
                output.add_page(page)
                output.write(outputStream)
        except Exception as e:
            return jsonify({"error": f"Error while merging or saving the PDF: {str(e)}"}), 500

        # Return the generated certificate
        try:
            return send_file(output_path, as_attachment=True)
        except Exception as e:
            return jsonify({"error": f"Error while sending the file: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
