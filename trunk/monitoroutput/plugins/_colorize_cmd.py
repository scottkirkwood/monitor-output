#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

import _plugin

ANSI_NORMAL = '\033[0m'   # Reset ANSI_NORMAL coloring
ansi_format = '\033[%sm'
color_templates = dict(
    Black= "0;30",
    Red = "0;31",
    Green = "0;32",
    Brown = "0;33",
    Blue = "0;34",
    Purple = "0;35",
    Cyan = "0;36",
    LightGray = "0;37",
    DarkGray = "1;30",
    LightRed = "1;31",
    LightGreen = "1;32",
    Yellow = "1;33",
    LightBlue = "1;34",
    LightPurple = "1;35",
    LightCyan = "1;36",
    White = "1;37",
  )

def getColor(color):
    return ansi_format % (color_templates[color])

class ColorizeCmd(_plugin.CommandPlugin):
    def __init__(self, color):
        self.color = color

    def __call__(self, match, line):
        ret = []
        if not match:
            return line

        ret.append(line[0:match.start()])
        ret.append(getColor(self.color))
        ret.append(match.group(0))
        ret.append(ANSI_NORMAL)
        ret.append(line[match.end():])

        return ''.join(ret)

class TestCommand(_plugin.TestCommand):
    def setUp(self):
        """ Setup self.instance here """
        self.instance = ColorizeCmd("Red")

    def testCommand(self):
        import re

        re_err = re.compile('Error')
        line  = "[Error]"
        match = re_err.search(line)
        ret = self.instance(match, line)
        self.assertEquals("[\033[0;31mError\033[0m]", ret)

    def testWholeLine(self):
        import re

        re_err = re.compile('Error')
        line  = "Error"
        match = re_err.search(line)
        ret = self.instance(match, line)
        self.assertEquals("\033[0;31mError\033[0m", ret)

    def testNothingToDo(self):
        import re

        re_err = re.compile('WontFindThisString')
        line  = "[Error]"
        match = re_err.search(line)
        ret = self.instance(match, line)
        self.assertEquals("[Error]", ret)

    def testFailCommand(self):
        import re
        bad_color = "ThisColorDoesntExist"
        self.instance = ColorizeCmd(bad_color)
        re_err = re.compile('Error')
        line  = "[Error]"
        match = re_err.search(line)
        try:
            ret = self.instance(match, line)
        except:
            pass
        else:
            self.fail("Should have failed for color %s" % (bad_color))

if __name__ == "__main__":
    import unittest
    unittest.main()
