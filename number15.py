import PyPDF2
import re
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pdfplumber

def increase_prices(text):
    # Define a regular expression pattern to match prices
    pattern = r'\$\s*\d+(\.\d{1,2})?'
    # Define a function to increase prices by 15%
    def increase(match):
        price = float(match.group().replace('$', '').replace(',', ''))
        new_price = price * 1.15
        return '${:,.2f}'.format(new_price)
    # Use re.sub() to replace prices in the text with the increased values
    return re.sub(pattern, increase, text)

def edit_pdf(input_path, output_path):
    # Open the input PDF file
    with pdfplumber.open(input_path) as pdf:
        writer = PyPDF2.PdfWriter()

        # Iterate through each page in the PDF
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text = page.extract_text()
            edited_text = increase_prices(text)

            # Create a new PDF page with the edited text
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.drawString(100, 100, edited_text)
            can.save()

            # Move to the beginning of the StringIO buffer
            packet.seek(0)
            new_pdf = PyPDF2.PdfReader(packet)
            page = new_pdf.pages[0]
            writer.add_page(page)

        # Write the modified PDF to the output file
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

# Example usage
edit_pdf('input.pdf', 'output.pdf')

print('pdf converted')

