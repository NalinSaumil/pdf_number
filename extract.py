import PyPDF2
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate

def increase_prices(text):
    # Define a regular expression pattern to match prices
    # pattern = r'\$\s*\d+(\.\d{1,2})?'
    pattern = r'\$\s*(\d{1,3}(,\d{3})*|\d+)(\.\d{1,2})?'

    # Define a function to increase prices by 15%
    def increase(match):
        price = float(match.group().replace('$', '').replace(',', ''))
        new_price = price * 1.15
        return '${:,.2f}'.format(new_price)
    # Use re.sub() to replace prices in the text with the increased values
    return re.sub(pattern, increase, text)

# Open the PDF file
with open('input.pdf', 'rb') as file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(file)
    # Extract text from each page
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

with open('extracted_text.txt', 'w', encoding='utf-8') as txt_file:
    txt_file.write(text)

print("Text extracted and saved into 'extracted_text.txt' file.")

text2 = increase_prices(text)

with open('extracted_text_2.txt', 'w', encoding='utf-8') as txt_file_2:
    txt_file_2.write(text2)

def create_pdf_from_text_with_formatting(text, output_filename):
    # Create a PDF document
    doc = SimpleDocTemplate(output_filename, pagesize=letter)

    # Create a stylesheet
    styles = getSampleStyleSheet()
    style_body = styles['Normal']

    # Create story to hold the text
    story = []

    # Add paragraphs to the story
    for line in text.split('\n'):
        if line.strip():
            para = Paragraph(line.strip(), style_body)
            story.append(para)

    # Build the PDF
    doc.build(story)

# Read the extracted text from the file
with open('extracted_text.txt', 'r', encoding='utf-8') as txt_file:
    extracted_text = txt_file.read()

# Create a PDF from the extracted text
create_pdf_from_text_with_formatting(extracted_text, 'output.pdf')

print("PDF recreated from extracted text and saved as 'recreated_pdf.pdf'.")

