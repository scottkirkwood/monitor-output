#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

import unittest

class MonitorPlugin:
    def __init__(self):
        self.events = [
        ]

    def name(self):
        """ This plugin's name """
        pass

    def description(self):
        """ Description for help """
        pass

    def search(self):
        pass

class CommandPlugin:
    def __call__(self, match, line):
        return line

class FakeCommandPlugin:
    def __init__(self, to_return):
        self.to_return = to_return

    def __call__(self, match, line):
        if match != None:
            return self.to_return
        return None # Return something else

class TestPlugin(unittest.TestCase):
    def setUp(self):
        """ Setup self.instance here """
        pass

class TestCommand(unittest.TestCase):
    def setUp(self):
        """ Setup self.instance here """
        pass
