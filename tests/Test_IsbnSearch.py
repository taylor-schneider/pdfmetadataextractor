from unittest import TestCase
import os
from PdfInspection import IsbnSearch


class test_IsbnSearch(TestCase):

    def __init__(self, *args, **kwargs):

        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.root_dir = os.path.dirname(self.current_directory)
        super(test_IsbnSearch, self).__init__(*args, **kwargs)

    def test__get_isbn_from_pdf__success_pdf_with_text_isbn(self):
        file_name = "Koha 3 Library Management - [Sirohi, Gupta] - 2010.pdf"
        file_path = os.path.join(self.root_dir, "tests", "pdfs", "With Text ISBN", file_name)
        isbns = IsbnSearch.find_isbns_in_pdf(file_path)
        self.assertEqual(["978-1-849510-82-0"], isbns)

    def test__get_isbn_from_pdf__success_pdf_with_text_no_isbn(self):
        file_name = "l3.pdf"
        file_path = os.path.join(self.root_dir, "tests", "pdfs", "With Text", file_name)
        isbns = IsbnSearch.find_isbns_in_pdf(file_path)
        self.assertEqual([], isbns)

    def test__get_isbn_from_pdf__success_pdf_with_no_ocr_text(self):
        file_name = "Solid Geometry.pdf"
        file_path = os.path.join(self.root_dir, "tests", "pdfs", "With No OCR Text", file_name)
        isbns = IsbnSearch.find_isbns_in_pdf(file_path)
        self.assertEqual([], isbns)

