#!/usr/bin/env python


import os
import argparse
from FileProcessing import ProcessFile


def run_deamon(args):

    directories = validate_args(args)

    # Get a list of files from the input directory that need to be processed
    file_names = os.listdir(directories["input"])
    file_paths_to_process = [os.path.join(directories["input"], file_name) for file_name in file_names]

    # Ignore hidden files
    file_paths_to_process = [file_path for file_path in file_paths_to_process if not os.path.basename(file_path).startswith(".")]

    # Do the work
    ProcessFile.process_files(file_paths_to_process, directories)


def create_arg_parser():
    parser = argparse.ArgumentParser(description='A PDF Metadata Collector')
    parser.add_argument('--input', help='The input directory where raw pdfs are uploaded for processing.', required=True)
    parser.add_argument('--wip', help='The directory where pdfs are kept as they are being processed.', required=True)
    parser.add_argument('--complete', help='The directory where fully processed pdfs are moved.', required=True)
    parser.add_argument('--reject', help='The directory where media is moved when it cannot be processed', required=True)
    return parser


def validate_args(args):
    # This function will make sure that the values supplied were valid.
    # An exception will be raised if the args are not valid
    try:

        directories = {
            "input": args.input,
            "wip": args.wip,
            "complete": args.complete,
            "reject": args.reject
        }

        for key in directories.keys():
            directory = directories[key]
            abs_path = os.path.abspath(directory)
            if not os.path.isdir(abs_path):
                raise Exception("The specified '{0}' directory '{1}' does not exist.".format(key, directory))
            if directory != abs_path:
                directories[key] = abs_path

        return directories

    except Exception as ex:
        raise Exception("The arguments could not be validated.") from ex

