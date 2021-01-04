from FileProcessing.pdf.PdfInspection import TextDetection, IsbnSearch
from FileProcessing import ProcessFile, VcsFile
import traceback
import os
import shutil

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

        # If we got more than one isbn we will have to narrow it down
        # We will need to lookup the data from sites and see if there are matches for things
        # eg. b-ok will list the title and authors and we will check if those are there
        isbn = isbns[0]

        # Create git repository and add file
        VcsFile.cleanup_old_wip(isbn, directories)
        VcsFile.create_repo_and_add_file(abs_file_path, isbn, directories)

        s = ""
        # Get metadata for isbn
        # Get isbn for isbn
        # Update marc with metadata (if necessary)

    except Exception:
        ex_string = traceback.format_exc()
        reason = "Exception was raised: {0}{1}".format(os.linesep, ex_string)
        ProcessFile.reject_file(abs_file_path, directories["reject"], reason)

