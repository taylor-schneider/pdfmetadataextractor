from Utils import get_lines_from_pdf_page
import re
from PyPDF2 import PdfFileReader

def find_isbn_number_in_line(possible_title):

    # The possible isbn formats are:
    #   ISBN 978-1-849510-82-0

    pattern = "ISBN.*"
    result = re.findall(pattern, possible_title)
    if len(result) > 0:
        s = ""

    pattern = '\d{3}-\d{1}-\d{1,6}-\d{1,6}-\d{1}'
    result = re.findall(pattern, possible_title)
    if len(result) > 0:
        return result[0]

#    pattern = "[0-9\\-]+"
#    result = re.findall(pattern, possible_title)
#    if len(result) > 0:
#        return result

    return None

def find_isbn_numbers_in_lines(possible_isbns):
    isbns = []
    for x in range(0, len(possible_isbns)):
        possible_isbn = possible_isbns[x]
        possible_isbn = possible_isbn.strip()
        isbn = find_isbn_number_in_line(possible_isbn)
        if isbn:
            isbns.append(isbn)
    return isbns

def find_isbns_in_pdf(file_path):

    try:
        # Open the pdf file and parse it
        with open(file_path, 'rb') as f:
            pdf = PdfFileReader(f)

            # Look at the text on the first few pages
            # If the pdf is shorter than the default number of pages to check,
            # we will adjust our search range
            number_of_pages_to_check = 5
            number_of_pages = pdf.getNumPages()

            if number_of_pages < number_of_pages_to_check:
                number_of_pages_to_check = number_of_pages

            # Look through each page for isbns
            isbns = []
            for x in range(1, number_of_pages_to_check):
                lines = get_lines_from_pdf_page(pdf, x)
                # Filter out lines that don't make sense
                new_isbns = find_isbn_numbers_in_lines(lines)
                if new_isbns:
                    isbns += new_isbns
            return isbns
    except Exception as e:
        raise Exception("An error occurred while trying to get ISBN numbers from a PDF.") from e
