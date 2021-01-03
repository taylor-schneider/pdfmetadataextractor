from unittest import TestCase
import os
import logging
import shutil
import sys
import daemon


# Configure logging format and level
log_format = '%(asctime)s,%(msecs)d %(levelname)-8s [%(module)s:%(funcName)s():%(lineno)d] %(message)s'
logging.basicConfig(format=log_format, datefmt='%Y-%m-%d:%H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger()


class Test_Deamon(TestCase):

    def __get_file_paths_from_dir(self, dir_abs_path):
        paths = []
        for dir_path, _, file_names in os.walk(dir_abs_path):
            for f in file_names:
                path = os.path.abspath(os.path.join(dir_path, f))
                paths.append(path)
        return paths

    def __get_pdfs_dir_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        pdf_directory = os.path.join(current_dir, 'pdfs')
        return pdf_directory

    def __get_demo_dir_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)
        demo_dir = os.path.join(root_dir, "demo")
        return demo_dir

    def __cleanup_demo_dir(self):
        logging.debug("Cleaning up demo dir.")
        demo_dir_path = self.__get_demo_dir_path()
        file_paths = self.__get_file_paths_from_dir(demo_dir_path)
        for file_path in file_paths:
            logging.debug("Removing file: {0}".format(file_path))
            os.remove(file_path)

    def __copy_file_to_dir(self, abs_file_path, absolute_dir_path):
        file_name = os.path.basename(abs_file_path)
        new_abs_file_path = os.path.join(absolute_dir_path, file_name)
        logging.debug("Copying '{0}' to {1}.".format(abs_file_path, new_abs_file_path))
        shutil.copy(abs_file_path, new_abs_file_path)

    def __copy_pdfs_to_demo_input(self):
        logging.debug("Copying pdfs to demo/input directory.")
        pdfs_dir_path = self.__get_pdfs_dir_path()
        demo_dir_path = self.__get_demo_dir_path()
        input_dir_path = os.path.join(demo_dir_path, "input")
        file_paths = self.__get_file_paths_from_dir(pdfs_dir_path)
        for file_path in file_paths:
            self.__copy_file_to_dir(file_path, input_dir_path)


    def test_deamon(self):
        # Get ready for the test
        self.__cleanup_demo_dir()
        self.__copy_pdfs_to_demo_input()

        # Set the args for the test
        logging.debug("Setting up test arguments")
        testargs = ["--input", "../demo/input", "--wip", "../demo/wip", "--complete", "../demo/complete", "--reject", "../demo/reject"]
        current_args = sys.argv
        sys.argv = [current_args[0]] + testargs

        # Run the daemon
        logging.debug("Running Daemon")
        daemon.main()

        # Check the correct files were rejected
        demo_dir_path = self.__get_demo_dir_path()
        reject_dir_path = os.path.join(demo_dir_path, "reject")
        rejected_file_paths = self.__get_file_paths_from_dir(reject_dir_path)
        self.assertEqual(1, len(rejected_file_paths))

