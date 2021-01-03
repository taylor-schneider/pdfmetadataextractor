from FileProcessing.pdf.PdfInspection import TextDetection, IsbnSearch
from FileProcessing import ProcessFile
import traceback
import os

def process_pdf(abs_file_path, directories):
    try:
        # Determine if the pdf has text
        has_text = TextDetection.pdf_has_text(abs_file_path, 0.95)

        # Reject the file if it has no text
        if not has_text:
            ProcessFile.reject_file(abs_file_path, directories["reject"], "No Text")
            return

        # Determine if the pdf has an isbn
        isbns = IsbnSearch.find_isbns_in_pdf(abs_file_path)
        if not isbns:
            ProcessFile.reject_file(abs_file_path, directories["reject"], "No ISBN")
            return

        # Create git repository and add file, and other files

        # Get metadata for isbn
        # Get isbn for isbn
        # Update marc with metadata (if necessary)

    except Exception:
        ex_string = traceback.format_exc()
        reason = "Exception was raised: {0}{1}".format(os.linesep, ex_string)
        ProcessFile.reject_file(abs_file_path, directories["reject"], reason)

