#!/usr/bin/env python

from mtools.util.logfile import LogFile
from mtools.util.logevent import LogEvent
from mtools.util.cmdlinetool import LogFileTool

import inspect
import mtools.mloginfo.sections as sections



class MLogInfoTool(LogFileTool):

    def __init__(self):
        """ Constructor: add description to argparser. """
        LogFileTool.__init__(self, multiple_logfiles=True, stdin_allowed=False)

        self.argparser.description = 'Extracts general information from logfile and prints it to stdout.'
        self.argparser.add_argument('--verbose', action='store_true', help='show more verbose output (depends on info section)')
        self.argparser_sectiongroup = self.argparser.add_argument_group('info sections', 'Below commands activate additional info sections for the log file.')

        # add all filter classes from the filters module
        self.sections = [c[1](self) for c in inspect.getmembers(sections, inspect.isclass)]

    def run(self, arguments=None):
        """ Print out useful information about the log file. """
        LogFileTool.run(self, arguments)

        for i, self.logfile in enumerate(self.args['logfile']):
            if i > 0:
                print
                print ' ------------------------------------------'
                print

            print "     source: %s" % self.logfile.name
            print "      start: %s" % (self.logfile.start.strftime("%Y %b %d %H:%M:%S") if self.logfile.start else "unknown")
            print "        end: %s" % (self.logfile.end.strftime("%Y %b %d %H:%M:%S") if self.logfile.start else "unknown")

            # TODO: add timezone if iso8601 format
            print "date format: %s" % self.logfile.datetime_format
            print "     length: %s" % len(self.logfile)
            print "     binary: %s" % (self.logfile.binary or "unknown")
            

            version = (' -> '.join(self.logfile.versions) or "unknown")

            # if version is unknown, go by date
            if version == 'unknown':
                if self.logfile.datetime_format == 'ctime-pre2.4':
                    version = '< 2.4 (no milliseconds)'
                elif self.logfile.datetime_format == 'ctime':
                    version = '>= 2.4 (milliseconds present)'
                elif self.logfile.datetime_format.startswith('iso8601-'):
                    version = '>= 2.6 (iso8601 format)'

            print "    version: %s" % version,
            print

            # now run all sections
            for section in self.sections:
                if section.active:
                    print
                    print section.name.upper()
                    section.run()


if __name__ == '__main__':
    tool = MLogInfoTool()
    tool.run()