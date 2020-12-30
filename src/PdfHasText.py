from PyPDF2 import PdfFileReader
import Utils

# These function will use the PdfFileReader class to open a pdf file.
# The class provides some metadata and functions which provide information about the files
# We will use them to determine if the PDF has text.

def pfd_has_ocr_text(file_path):

    # It is possible that a pdf has text in some places but not a majority of the content
    # For example an old physical book that was scanned by google;
    # It will have a preface with google text but the subsequent pages will all be jpgs.
    #
    # This function will return true if it finds text on a majority of the pages.
    #
    # The determination of whether or not text is present is based on the text
    # that the PdfFileReader extracts from a given page.

    try:
        with open(file_path, 'rb') as f:
            pdf = PdfFileReader(f)
            number_of_pages = pdf.getNumPages()
            interval = int(number_of_pages * 0.05)
            pages_to_check = range(0, number_of_pages, interval)
            pages_with_text = 0
            pages_checked = 0
            for page_number in pages_to_check:
                lines = Utils.get_lines_from_pdf_page(f, page_number)
                if len(lines) > 0:
                    pages_with_text += 1
                pages_checked += 1

            # Determine if enough pages had text
            required_percentage_with_text = 0.95
            actual_percentage_with_text = pages_with_text / pages_checked
            if actual_percentage_with_text >= required_percentage_with_text:
                return True
            else:
                return False
    except Exception as e:
        raise Exception("Unable to determine if pdf has OCR text.") from e

def pfd_has_ocr_text2(file_path):

    # It is possible that a pdf has text in some places but not a majority of the content
    # For example an old physical book that was scanned by google;
    # It will have a preface with google text but the subsequent pages will all be jpgs
    #
    # This function will return true if it finds text on a majority of the pages
    #
    # The determination of whether or not text is present is based on the metadata
    # about the page that is stored in the pdf.
    #
    # This method is less reliable.

    try:
        with open(file_path, 'rb') as f:
            pdf = PdfFileReader(f)
            number_of_pages = pdf.getNumPages()
            interval = int(number_of_pages * 0.05)
            pages_to_check = range(0, number_of_pages, interval)
            pages_with_text = 0
            pages_checked = 0
            for page_number in pages_to_check:

                page_data = pdf.getPage(page_number)
                if '/Font' in page_data['/Resources']:
                    pages_with_text += 1
                pages_checked += 1

            # Determine if enough pages had text
            required_percentage_with_text = 0.90
            actual_percentage_with_text = pages_with_text / pages_checked
            if actual_percentage_with_text >= required_percentage_with_text:
                return True
            else:
                return False
    except Exception as e:
        raise Exception("Unable to determine if pdf has OCR text.") from e