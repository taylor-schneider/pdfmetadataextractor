import os
import logging
from FileProcessing.pdf.PdfProcessing import ProcessPdf

def move_file_to_dir(abs_file_path, absolute_dir_path):
    file_name = os.path.basename(abs_file_path)
    new_abs_file_path = os.path.join(absolute_dir_path, file_name)
    logging.debug("Moving '{0}' to {1}.".format(abs_file_path, new_abs_file_path))
    os.rename(abs_file_path, new_abs_file_path)


def reject_file(abs_file_path, reject_dir, reason):
    logging.debug("Rejecting '{0}'. Reason: {1}".format(abs_file_path, reason))
    move_file_to_dir(abs_file_path, reject_dir)


def process_file(abs_file_path, directories):

    # Reject any unsupported files
    supported_extensions = [".pdf"]
    file_name, file_extension = os.path.splitext(abs_file_path)
    if file_extension not in supported_extensions:
        reject_file(abs_file_path, directories["reject"], "Unsupported file extension")
        return

    # Process the file
    if file_extension == ".pdf":
        ProcessPdf.process_pdf(abs_file_path, directories)



def process_files(abs_file_paths, directories):
    for abs_file_path in abs_file_paths:
        process_file(abs_file_path, directories)
