"""cl.bin.base"""

from __future__ import absolute_import

import optparse
import os
import sys

from .. import __version__

__all__ = ["Option", "Command"]
Option = optparse.make_option


class Command(object):
    Parser = optparse.OptionParser

    args = ''
    version = __version__
    option_list = ()

    def run(self, *args, **options):
        raise NotImplementedError("subclass responsibility")

    def execute_from_commandline(self, argv=None):
        """Execute application from command line.

        :keyword argv: The list of command line arguments.
                       Defaults to ``sys.argv``.

        """
        if argv is None:
            argv = list(sys.argv)
        prog_name = os.path.basename(argv[0])
        return self.handle_argv(prog_name, argv[1:])

    def usage(self):
        """Returns the command-line usage string for this app."""
        return "%%prog [options] %s" % (self.args, )

    def get_options(self):
        """Get supported command line options."""
        return self.option_list

    def handle_argv(self, prog_name, argv):
        """Parses command line arguments from ``argv`` and dispatches
        to :meth:`run`.

        :param prog_name: The program name (``argv[0]``).
        :param argv: Command arguments.

        Exits with an error message if :attr:`supports_args` is disabled
        and ``argv`` contains positional arguments.

        """
        options, args = self.parse_options(prog_name, argv)
        return self.run(*args, **vars(options))

    def parse_options(self, prog_name, arguments):
        """Parse the available options."""
        # Don't want to load configuration to just print the version,
        # so we handle --version manually here.
        if "--version" in arguments:
            print(self.version)
            sys.exit(0)
        parser = self.create_parser(prog_name)
        options, args = parser.parse_args(arguments)
        return options, args

    def create_parser(self, prog_name):
        return self.Parser(prog=prog_name,
                           usage=self.usage(),
                           version=self.version,
                           option_list=self.get_options())
