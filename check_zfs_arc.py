#!/usr/bin/env python

"""
Nagios/Icinga plugin to monitor the ARC usage on a ZFS enabled system

authors:
    Mattia Martinello - mattia@mattiamartinello.com
"""

_VERSION = '1.0'
_VERSION_DESCR = 'Monitors the ARC usage on a ZFS enabled system.'

import argparse
from datetime import datetime
import logging
import sys
import re
import time

ICINGA_OK = 0
ICINGA_WARNING = 1
ICINGA_CRITICAL = 2
ICINGA_UNKNOWN = 3
ICINGA_LABELS = {0: 'OK', 1: 'WARNING', 2: 'CRITICAL', 3: 'UNKNOWN'}

def icinga_exit(level, details=None, perfdata=[]):
    """Exit to system producing an output conform
    to the Icinga standards.
    """
    # choose the right stream
    stream = sys.stdout if level == ICINGA_OK else sys.stderr

    # build the message as level + details
    msg = ICINGA_LABELS.get(level)
    if details:
        msg = '{} - {}'.format(msg, details)

    # add perfata if given
    if len(perfdata):
        perfdata_string = ' '.join(perfdata)
        msg = '{} |{}'.format(msg, perfdata_string)

    # exit with status and message
    print(msg, file=stream)
    sys.exit(level)

def exit_with_error(message):
    """Exit with the Icinga Unknown status code and the given error
    """

    message = 'ERROR: {}'.format(message)
    icinga_exit(ICINGA_UNKNOWN, message)


class Checker:
    """Parse the command line, run checks and return status.
    """

    def __init__(self):
        # init the cmd line parser
        parser = argparse.ArgumentParser(
            description='Icinga plugin: check_pve_backups'
        )
        self.add_arguments(parser)

        # read the command line
        args = parser.parse_args()

        # manage arguments
        self._manage_arguments(args)

    def add_arguments(self, parser):
        """Add command arguments to the argument parser.
        """

        parser.add_argument(
            '-V', '--version',
            action='version',
            version = '%(prog)s v{} - {}'.format(_VERSION, _VERSION_DESCR)
        )

        parser.add_argument(
            '--debug',
            action="store_true",
            help='Print debugging info to console. This may make the plugin '
                 'not working with Icinga since it prints stuff to console.'
        )

        parser.add_argument(
            '-w', '--warning',
            dest='warning',
            type=int,
            help='Warning threshold in bytes or percentage of the total RAM'
        )

        parser.add_argument(
            '-c', '--critical',
            dest='critical',
            type=int,
            help='Critical threshold in bytes or percentage of the total RAM'
        )

    def _manage_arguments(self, args):
        """Get command arguments from the argument parser and load them.
        """

        # debug flag
        self.debug = getattr(args, 'debug', False)

        # print arguments (debug)
        logging.debug('Command arguments: {}'.format(args))

        # Warning threshold in bytes or percentage of the total RAM
        self.warning = getattr(args, 'warning')

        # Critical threshold in bytes or percentage of the total RAM
        self.critical = getattr(args, 'critical')

    def _get_ram_total(self, input_text=None):
        pattern = '^MemTotal:\s+([0-9]+) kB$'
        matches = re.search(pattern, input_text, re.MULTILINE)

        try:
            ram_total_kb = int(matches.group(1))
            ram_total = ram_total_kb * 1024
            return ram_total
        except:
            return None

    def handle(self):
        """Connect to Proxmox API, start the requested check and give result.
        """

        pass


if __name__ == "__main__":
    # run the procedure and get results: if I get an exception I exit with
    # the Icinga UNKNOWN status code
    main = Checker()
    main.handle()
