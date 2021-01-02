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

        result1 = PdfHasText.pfd_has_ocr_text1(file_path)
        result2 = PdfHasText.pfd_has_ocr_text2(file_path)
        result3 = PdfHasText.pfd_has_ocr_text3(file_path)

        self.assertEqual(False, result1)
        self.assertEqual(False, result2)
        self.assertEqual(False, result3)

    def test__pfd_has_ocr_text__true__1(self):
        file_name = "Koha 3 Library Management - [Sirohi, Gupta] - 2010.pdf"
        file_path = os.path.join(self.root_dir, "tests", "pdfs", "With Text ISBN", file_name)

        result1 = PdfHasText.pfd_has_ocr_text1(file_path)
        result2 = PdfHasText.pfd_has_ocr_text2(file_path)
        result3 = PdfHasText.pfd_has_ocr_text3(file_path)

        self.assertEqual(True, result1)
        self.assertEqual(True, result2)
        self.assertEqual(True, result3)

    def test__pfd_has_ocr_text__true__2(self):
        file_name = "l3.pdf"
        file_path = os.path.join(self.root_dir, "tests", "pdfs", "With Text", file_name)

        result1 = PdfHasText.pfd_has_ocr_text1(file_path)
        result2 = PdfHasText.pfd_has_ocr_text2(file_path)
        result3 = PdfHasText.pfd_has_ocr_text3(file_path)

        self.assertEqual(True, result1)
        self.assertEqual(True, result2)
        self.assertEqual(True, result3)
