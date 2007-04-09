#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

import unittest
import re

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
  

class MonitorPlugin:
  def __init__(self):
    self.events = [
      dict(
        params = re.IGNORECASE,
        greps = [ 'Error'],
        unless = [],
        commands = [ Colorize(color="Red"),],
      ),
      dict(
        params = re.IGNORECASE,
        greps = [ 'Hey'],
        unless = [],
        commands = [ Notify(message="Hey Man"),],
      ),
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
  
class Colorize(CommandPlugin):
  def __init__(self, color):
    self.color = color
  
  def __call__(self, match, line):
    ret = []
    ret.append(line[0:match.start()])
    ret.append(getColor(self.color))
    ret.append(match.group(0))
    ret.append(ANSI_NORMAL)
    ret.append(line[match.end():])
    return ''.join(ret)

class Notify(CommandPlugin):
  def __init__(self, message):
    self.message = message
  
  def __call__(self, match, line):
    import pynotify
    
    if not pynotify.is_initted():
      pynotify.init('monitor-output-notify')
    self.notify = pynotify.Notification(self.message, 'xyz')
    self.notify.show()
    return line

class TestPlugin(unittest.TestCase):
  def setUp(self):
    """ Setup self.instance here """
    pass
    
