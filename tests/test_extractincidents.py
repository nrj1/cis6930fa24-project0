# # import os
# # from pypdf import PdfWriter
# # from project0.main import extract_text_from_pdf

# # def create_dummy_pdf(filename, text):
# #     filepath = os.path.join(r"C:\Users\Rajeev\Desktop\Git-Hub Projects\cis6930fa24-project0\tmp", filename)
# #     writer = PdfWriter()
# #     writer.add_blank_page(width=595, height=842)
# #     with open(filepath, "wb") as f:
# #         writer.write(text)

# #     return filepath

# # def test_extract_text_from_pdf():
# #     filename = "test.pdf"
# #     dummy_text = "This is a test"
    
# #     # Create a dummy PDF
# #     create_dummy_pdf(filename, dummy_text)
    
# #     # Test extraction
# #     extracted_text = extract_text_from_pdf(filename)
    
# #     assert dummy_text in extracted_text, "Text extraction failed"
    
# #     # Clean up
# #     filepath = os.path.join(r"C:\Users\Rajeev\Desktop\Git-Hub Projects\cis6930fa24-project0\tmp", filename)
# #     os.remove(filepath)




# import os
# from pypdf import PdfWriter, PdfReader
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from io import BytesIO
# from project0.main import extract_text_from_pdf

# def create_dummy_pdf(filename, text):
#     filepath = os.path.join(r"C:\Users\Rajeev\Desktop\Git-Hub Projects\cis6930fa24-project0\tmp", filename)
    
    
#     # Create a PDF with reportlab
#     packet = BytesIO()
#     can = canvas.Canvas(packet, pagesize=letter)
#     can.drawString(100, 750, text)
#     can.save()
    
#     # Move to the beginning of the StringIO buffer
#     packet.seek(0)
#     new_pdf = PdfReader(packet)
    
#     # Create a new PDF with pypdf
#     output = PdfWriter()
    
#     # Add the "watermark" (which is the new pdf) on the existing page
#     page = new_pdf.pages[0]
#     output.add_page(page)
    
#     # Finally, write "output" to a real file
#     with open(filepath, "wb") as outputStream:
#         output.write(outputStream)

#     return filepath

# def test_extract_text_from_pdf():
#     filename = "test.pdf"
#     dummy_text = "This is a test"
    
#     # Create a dummy PDF
#     pdf_path = create_dummy_pdf(filename, dummy_text)
    
#     # Now you can test your extract_text_from_pdf function
#     extracted_text = extract_text_from_pdf(filename)  # Assuming this function exists
#     assert dummy_text in extracted_text, "Extracted text does not match the input text"

import os
from pypdf import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from project0.main import extract_text_from_pdf

def create_dummy_pdf(filename, text):
    # Get the path to the tmp directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    tmp_dir = os.path.join(parent_dir, 'tmp')
    
    # Ensure tmp directory exists
    os.makedirs(tmp_dir, exist_ok=True)
    
    filepath = os.path.join(tmp_dir, filename)
    
    # Create a PDF with reportlab
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(100, 750, text)
    can.save()
    
    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfReader(packet)
    
    # Create a new PDF with pypdf
    output = PdfWriter()
    
    # Add the "watermark" (which is the new pdf) on the existing page
    page = new_pdf.pages[0]
    output.add_page(page)
    
    # Finally, write "output" to a real file
    with open(filepath, "wb") as outputStream:
        output.write(outputStream)

    return filepath

def test_extract_text_from_pdf():
    filename = "test.pdf"
    dummy_text = "This is a test"
    
    # Create a dummy PDF
    pdf_path = create_dummy_pdf(filename, dummy_text)
    
    # Now you can test your extract_text_from_pdf function
    extracted_text = extract_text_from_pdf(pdf_path)  # Pass the full path
    assert dummy_text in extracted_text, "Extracted text does not match the input text"
    
    # Clean up
    os.remove(pdf_path)