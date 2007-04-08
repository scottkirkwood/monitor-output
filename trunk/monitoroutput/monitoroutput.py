#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

"""
Monitor the output of a program then cause an event to happen
"""

__author__ = 'scottakirkwood@gmail.com (Scott Kirkwood)'

import re
import os
import sys
import subprocess

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
  
class MonitorOutput:
  def __init__(self):
    self.args = ['cat', 'test_message.txt']
    self.events = [
      {
        'greps' : [dict(
            regex ='Error', 
            params = re.IGNORECASE,
          ),
          ],  
        # How to do functional programing
        'commands' : [
          (self.colorize, dict(color = "Red", regex = [dict(regex='Error', params = re.IGNORECASE)]))
        ],
      },
    ]
  
  def run(self, arguments):
    args = self.args
    p = subprocess.Popen(args, 
        stdout=subprocess.PIPE, close_fds=True)
    output = p.stdout
    for line in output:
      for event in self.events:
        args = self.search(event, line)
        if args:
          line = self.run_events(event, args, line)
      
      sys.stdout.write(line)
      
  def search(self, event, line):
    """ Returns true if part matches """
    found_groups = None
    for grep in event['greps']:
      args = self._search_grep(grep, line)
      if args:
        found_groups = args
        break
    return found_groups
    
  def _search_grep(self, grepinfo, line):
    if 'compiled_re' not in grepinfo:
      params = None
      if 'params' in grepinfo:
        params = grepinfo['params']
      grepinfo['compiled_re'] = re.compile(grepinfo['regex'], params)
    
    return grepinfo['compiled_re'].search(line)
    
  def colorize(self, dict):
    groups = dict['groups']
    line = dict['line']
    ret = []
    ret.append(line[0:groups.start()])
    ret.append(getColor(dict['color']))
    ret.append(groups.group(0))
    ret.append(ANSI_NORMAL)
    ret.append(line[groups.end():])
    return ''.join(ret)
    
  def run_events(self, event, groups, line):
    """ Execute the event, possibly modifying the line """
    for cmd in event['commands']:
      cmd[1]['line'] = line
      cmd[1]['groups'] = groups
      line = cmd[0](cmd[1])
    return line
    
def parse_command_line():
    monitor_output = MonitorOutput()
    monitor_output.run(sys.argv)

if __name__ == "__main__":
    parse_command_line()
