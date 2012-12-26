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
        self.args = None

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
        self.args, self.argv = parser.parse_known_args(self.argv)
        args = self.args
        target = self.args.target
        del self.args.target
        log.set_verbosity(args.verbose)
        parser._remove_action(fake_action)

        parser.add_argument(
            '-h', '--help', action='store_true',
            help='show this help message and exit')
        if target is None:
            # consume the 'help' argument
            self.args, self.argv = parser.parse_known_args(self.argv, self.args)
        self.subparser = parser.add_subparsers(help="target help", dest="target")

        self.load(args.file, target=target)

    def print_help(self):
        self.arg_parser.print_help()
        self.arg_parser.exit()

    def add_task(self, task, default=False):
        self.manage.add(task, default)

    def invoke_task(self, task):
        self.manage.invoke(task)

    def load(self, vakefile, target=None):
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
