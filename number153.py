import PyPDF2
import re
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def increase_numbers_by_percentage(pdf_file_path, output_file_path, increase_percentage=15):
    # Open the PDF file
    with open(pdf_file_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        # Create a PDF writer object
        pdf_writer = PyPDF2.PdfWriter()

        # Iterate through each page of the PDF
        for page_num in range(len(pdf_reader.pages)):
            # Get the page object
            page = pdf_reader.pages[page_num]
            # Extract text from the page
            text = page.extract_text()

            # Use regular expression to find and modify numbers (prices)
            modified_text = re.sub(r'\d+(\.\d+)?', lambda x: str(round(float(x.group(0)) * (1 + increase_percentage/100), 2)), text)

            # Create a new PDF page with the edited text
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.drawString(100, 100, modified_text)
            can.save()

            # Move to the beginning of the StringIO buffer
            packet.seek(0)
            new_pdf = PyPDF2.PdfReader(packet)
            page = new_pdf.pages[0]

            # Add the new page to the PDF writer object
            pdf_writer.add_page(page)

        # Write the modified PDF to a new file
        with open(output_file_path, 'wb') as output_file:
            pdf_writer.write(output_file)

# Example usage
input_pdf_path = 'input.pdf'
output_pdf_path = 'output_invoice.pdf'
increase_percentage = 15

increase_numbers_by_percentage(input_pdf_path, output_pdf_path, increase_percentage)
