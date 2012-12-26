# -*- coding: utf-8 -*-

import sys
import argparse

from os import path as ospath
from vake import log

from .manage import TaskManage
from .utils import import_module

class VakeFileNotExist(Exception):
    pass

class Application(object):
    def __init__(self):
        self.manage = TaskManage()
        self.arg_parser = self._create_arg_parser()
        self.subparser = None
        self.argv = sys.argv[1:]
        self.options = None

    def _create_arg_parser(self):
        parser = argparse.ArgumentParser(
                description="Python Makefile System", 
                prog="vake", add_help=False)
        parser.add_argument(
                '-f', '--file', 
                type=str, default='vakefile',
                help='specified a vakefile')
        parser.add_argument(
                '-v', '--verbose', 
                type=int, choices=[0, 1, 2], default=1)
        return parser

    def main(self):
        parser = self.arg_parser

        fake_action = parser.add_argument(
            'target', type=str, nargs='?', default=None)
        self.options, self.argv = parser.parse_known_args(self.argv)
        options = self.options
        target = self.options.target
        del self.options.target
        log.set_verbosity(options.verbose)
        parser._remove_action(fake_action)

        parser.add_argument(
            '-h', '--help', action='store_true',
            help='show this help message and exit')
        if target is None:
            # consume the 'help' argument
            self.options, self.argv = parser.parse_known_args(self.argv, self.options)
        self.subparser = parser.add_subparsers(help="target help", dest="target")

        self.load(options.file, target=target)

    def main(self):
        parser = self.arg_parser
        # parse options --file and verbos
        self.options, self.argv = parser.parse_known_args(self.argv)
        log.set_verbosity(self.options.verbose)
        parser.add_argument(
            '-h', '--help', action='help', default=argparse.SUPPRESS,
            help='show this help message and exit')
        self.subparser = parser.add_subparsers(help='target help', dest='target')

        file = self.options.file
        if file is None:
            if ospath.isfile('vakefile.py'):
                file = 'vakefile.py'
            else:
                self.print_help_and_exit()
        self.load(self.options.file)

    def print_help_and_exit(self):
        self.arg_parser.print_help()
        self.arg_parser.exit()

    def add_task(self, task, default=False):
        self.manage.add(task, default)

    def invoke_task(self, task):
        self.manage.invoke(task)

    def load(self, vakefile):
		if len(self.argv) == 0:
			target = self.manage.default
			if target is None:
				self.print_help_and_exit()
		else:
			options, argv = self.arg_parser.parse_known_args(self.argv, self.options)
			target = options.target
        path = ospath.abspath(vakefile)
        if not ospath.exists(path):
            raise VakeFileNotExist("Vake file '%s' is not exists" % path)
        directory, filename =  ospath.split(path)
        name, ext = ospath.splitext(filename)

        sys.path.insert(0, directory)

        parser = self.arg_parser

        import_module(name)

        if target is None and self.args.help:
            self.print_help()
        if target is None:
            task = self.manage.default
            if task is None:
                self.print_help()
            target = task.name
        self.argv.insert(0, target)
        self.args, self.argv = parser.parse_known_args(self.argv, self.args)

        self.manage.invoke(target)

app = Application()
