from PyPDF2 import PdfFileReader
import Utils


# These functions will use the PdfFileReader class to open a pdf file.
# The class provides some metadata and functions which provide information about the files
# We will use them to determine if the PDF has text.


def __determine_how_many_pages_must_have_text(number_of_pages, significance_level):
    required_percentage_with_text = 1 - significance_level
    required_number_text_pages = int(number_of_pages * required_percentage_with_text)
    return required_number_text_pages


def pfd_has_ocr_text1(file_path, significance_level=.95):

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

            # Open the pdf
            pdf = PdfFileReader(f)

            # Check how many pages have text
            number_of_pages = pdf.getNumPages()
            required_number_text_pages = __determine_how_many_pages_must_have_text(number_of_pages, significance_level)
            pages_with_text = 0
            for page_number in range(0, number_of_pages):
                lines = Utils.get_lines_from_pdf_page(f, page_number)
                if len(lines) > 0:
                    pages_with_text += 1
                if pages_with_text >= required_number_text_pages:
                    return True

            # If we got here, not enough pages had text
            return False

    except Exception as e:
        raise Exception("Unable to determine if pdf has OCR text.") from e

def pfd_has_ocr_text2(file_path, significance_level=.95):

    # The determination of whether or not text is present is based on the metadata
    # about the page that is stored in the pdf.
    #
    # This method is much faster than the original function
    # but it may also be less reliable

    try:
        with open(file_path, 'rb') as f:

            # Open the pdf
            pdf = PdfFileReader(f)

            # Check how many pages have text
            number_of_pages = pdf.getNumPages()
            required_number_text_pages = __determine_how_many_pages_must_have_text(number_of_pages, significance_level)
            pages_with_text = 0
            for page_number in range(0, number_of_pages):
                page_data = pdf.getPage(page_number)
                if '/Font' in page_data['/Resources']:
                    pages_with_text += 1
                if pages_with_text >= required_number_text_pages:
                    return True

            # If we got here, not enough pages had text
            return False

    except Exception as e:
        raise Exception("Unable to determine if pdf has OCR text.") from e

def pfd_has_ocr_text3(file_path, significance_level=.95):

    # This is a hybrid between the other two methods
    # The determination of whether or not text is present is based on the metadata
    # about the page that is stored in the pdf and/or the text
    #
    # This method can be faster than the original function
    # but it may also be less reliable

    try:
        with open(file_path, 'rb') as f:

            # Open the pdf
            pdf = PdfFileReader(f)

            # Check how many pages have text
            number_of_pages = pdf.getNumPages()
            required_number_text_pages = __determine_how_many_pages_must_have_text(number_of_pages, significance_level)
            pages_with_text = 0
            for page_number in range(0, number_of_pages):
                a = Utils.page_has_font_resource(pdf, page_number)

                if a:
                    pages_with_text += 1
                else:
                    b = Utils.page_has_text(pdf, page_number)
                    if b:
                        pages_with_text += 1

                if pages_with_text >= required_number_text_pages:
                    return True

            # If we got here, not enough pages had text
            return False

    except Exception as e:
        raise Exception("Unable to determine if pdf has OCR text.") from e


