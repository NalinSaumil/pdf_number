import PyPDF2
import re
import fitz  # PyMuPDF

def increase_prices_in_pdf(input_pdf_path, output_pdf_path):
    # Open the PDF file
    pdf_reader = PyPDF2.PdfFileReader(open(input_pdf_path, "rb"))

    # Create a PDF writer object
    pdf_writer = PyPDF2.PdfFileWriter()

    # Iterate through each page of the PDF
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)

        # Extract text from the page using PyMuPDF
        doc = fitz.open(input_pdf_path)
        page_text = doc[page_num].get_text()

        # Use regex to find and replace prices
        updated_text = re.sub(r'\b(\d+\.\d+)\b', lambda x: f'{float(x.group(0)) * 1.15:.2f}', page_text)

        # Add the updated text to the page
        page = PyPDF2.pdf.PageObject.create_text_object(page, updated_text)

        # Add the updated page to the PDF writer
        pdf_writer.add_page(page)

    # Write the updated PDF to a new file
    with open(output_pdf_path, "wb") as output_pdf_file:
        pdf_writer.write(output_pdf_file)

    print("PDF with increased prices has been generated successfully.")

# Example usage:
input_pdf_path = "input.pdf"
output_pdf_path = "output_invoice.pdf"
increase_prices_in_pdf(input_pdf_path, output_pdf_path)
