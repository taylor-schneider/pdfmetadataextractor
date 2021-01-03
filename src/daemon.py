#!/usr/bin/env python

'''
This script hosts a daemon which will process PDFs and collect relevant metadata.
It will move files between directories while it is working:
    1. Input
    2. WIP
    3. Complete
    4. Reject

The basic process is as follows:

    Scan the input directory for pdf files
    For each File pdf file
        Create vcs repository in WIP if it does not exist
            Add Checklist
            Add log file


The script can be run as follows:
    daemon.py --input ../demo/input --wip ../demo/wip --complete ../demo/complete --reject ../demo/reject

'''

import logging
import daemon_utils

# Configure logging format and level
log_format = '%(asctime)s,%(msecs)d %(levelname)-8s [%(module)s:%(funcName)s():%(lineno)d] %(message)s'
logging.basicConfig(format=log_format, datefmt='%Y-%m-%d:%H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger()


def main():
    parser = daemon_utils.create_arg_parser()
    args = parser.parse_args()
    daemon_utils.run_deamon(args)

if __name__ == '__main__':
    main()


