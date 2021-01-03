from PyPDF2 import PdfFileReader
import os
import io


def get_lines_from_pdf(pdf, page_number):

    # Extract the text from the page
    page = pdf.getPage(page_number)
    page_text = page.extractText()

    # Figure out which line separator to use
    # The book may have been published in a different OS
    # and using different carriage returns
    line_sep = os.linesep
    if os.linesep not in page_text:
        line_sep = "\n"

    lines = [line for line in page_text.split(line_sep) if line]
    return lines

def get_lines_from_pdf_page(o, page_number):

    try:
        # Determine what type of type of object we are dealing with
        # It could be a buffer, pdf, or file path
        if isinstance(o, io.BufferedIOBase):
            pdf = PdfFileReader(o)
            return get_lines_from_pdf(pdf, page_number)
        elif type(o) == PdfFileReader:
            pdf = o
            return get_lines_from_pdf(pdf, page_number)
        elif type(o) == str:
            file_path = o
            with open(file_path, 'rb') as f:
                pdf = PdfFileReader(f)
                return get_lines_from_pdf(pdf, page_number)
        else:
            raise Exception("The type supplied was not valid.")
    except Exception as e:
        raise Exception("Unable to get lines from pdf page.") from e

def page_has_text(pdf, page_number):
    lines = get_lines_from_pdf_page(pdf, page_number)
    return len(lines) > 0

def page_has_font_resource(pdf, page_number):
    page_data = pdf.getPage(page_number)
    return '/Font' in page_data['/Resources']