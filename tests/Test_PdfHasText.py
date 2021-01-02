from unittest import TestCase
import PdfHasText
import os

class test_PdfHasText(TestCase):

    def __init__(self, *args, **kwargs):

        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.root_dir = os.path.dirname(self.current_directory)
        super(test_PdfHasText, self).__init__(*args, **kwargs)

    def test__pfd_has_ocr_text__false(self):
        file_name = "Solid Geometry.pdf"
        file_path = os.path.join(self.root_dir, "tests", "pdfs", "With No OCR Text", file_name)
        result = PdfHasText.pfd_has_ocr_text2(file_path)
        self.assertEqual(False, result)

    def test__pfd_has_ocr_text__true__1(self):
        file_name = "Koha 3 Library Management - [Sirohi, Gupta] - 2010.pdf"
        file_path = os.path.join(self.root_dir, "tests", "pdfs", "With Text ISBN", file_name)
        result = PdfHasText.pfd_has_ocr_text2(file_path)
        self.assertEqual(True, result)

    def test__pfd_has_ocr_text__true__2(self):
        file_name = "l3.pdf"
        file_path = os.path.join(self.root_dir, "tests", "pdfs", "With Text", file_name)
        result = PdfHasText.pfd_has_ocr_text2(file_path)
        self.assertEqual(True, result)