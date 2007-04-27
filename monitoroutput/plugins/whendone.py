#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

"""
Show a notify when the program exists
"""

import monitoroutput.monitoroutput
import _plugin
import _notify_cmd
import re

def create_plugin():
    return WhenDonePlugin()

class WhenDonePlugin(_plugin.MonitorPlugin):
    def __init__(self):
        _plugin.MonitorPlugin.__init__(self)

        self.events = [
          dict(
            name='Finished',
            event='exit',
            commands = [
             _notify_cmd.NotifyCmd(
                message=r"Program has exited"),],
          ),
        ]

    def name(self):
        """ This plugin's name """
        return "whendone"

    def description(self):
        """ Description for help """
        return "Notify when the program exists"

if __name__ == "__main__":
    import unittest
    unittest.main()
