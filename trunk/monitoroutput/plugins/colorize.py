#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

import monitoroutput.monitoroutput
import _plugin
import _colorize_cmd
import _notify_cmd
import re

def create_plugin():
  return ColorizePlugin()
  
class ColorizePlugin(_plugin.MonitorPlugin):
  def __init__(self):
    _plugin.MonitorPlugin.__init__(self)
    
    self.events = [
      dict(
        params = re.IGNORECASE,
        greps = [ 'Error', r'Exception in thread \"'],
        unless = [],
        commands = [ _notify_cmd.NotifyCmd(subject="Monitor Output", 
            message="Error occured"),],
      ),
      dict(
        greps = [ 'WARNING:'],
        unless = [],
        commands = [ _colorize_cmd.ColorizeCmd(color="Blue"),],
      ),
      dict(
        params = re.IGNORECASE,
        greps = [ 'Hey'],
        unless = [],
        commands = [ _notify_cmd.NotifyCmd(subject="Monitor Output", 
            message="Error occured"),],
      ),
      dict(
        params = re.IGNORECASE,
        greps = [r'\s(\S+)\sinitialized and serving traffic'],
        unless = [],
        commands = [ _notify_cmd.NotifyCmd(subject="Monitor Output", 
            message="%(group1)s started and serving traffic"),],
      ),
    ]
    
  def name(self):
    """ This plugin's name """
    return "colorize"
    
  def description(self):
    """ Description for help """
    return "given a regex turn the text a certain color using ANSI text"
    
  def search(self):
    pass
  
class TestPlugin(_plugin.TestCommand):
  def setUp(self):
    """ Setup self.instance here """
    self.mo = monitoroutput.monitoroutput.MonitorOutput()
    self.instance = ColorizePlugin()
    self.mo.curplugin = self.instance
    
  def testServingTraffic(self):
    line = "070419 19:07:11.861:I 40 [Thread-12] [com2.run] AXTE initialized and serving traffic"
    self.mo.handle_line(line)

  def testWarning(self):
    line = "] WARNING: blabla"
    out = self.mo.handle_line(line)
    self.assertEquals('] \033[0;34mWARNING:\033[0m blabla', out)

  def testThreadWarning(self):
    line = 'Exception in thread "main" com.google.common.base.Flags$FlagUpdateError: '
    out = self.mo.handle_line(line)
    
if __name__ == "__main__":
  import unittest
  unittest.main()
