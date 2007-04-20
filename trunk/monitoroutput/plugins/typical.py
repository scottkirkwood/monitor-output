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
  return DefaultPlugin()
  
class DefaultPlugin(_plugin.MonitorPlugin):
  def __init__(self):
    _plugin.MonitorPlugin.__init__(self)
    
    self.events = [
      dict(
        name='Thread Exception',
        params = re.IGNORECASE,
        greps = [ 'Error', r'Exception in thread \"'],
        unless = [],
        commands = [ _notify_cmd.NotifyCmd(
            message="Error occured"),],
      ),
      dict(
        name='Warning',
        greps = [ r'(.*\sWARNING:.*)'],
        unless = [],
        commands = [ _colorize_cmd.ColorizeCmd(color="Blue"),],
      ),
      dict(
        name='Warning',
        params = re.IGNORECASE,
        greps = [ r'(.*\sERROR:.*)'],
        unless = [],
        commands = [ _notify_cmd.NotifyCmd(
            message="Error occured"),],
      ),
      dict(
        name='Started',
        params = re.IGNORECASE,
        greps = [r'\s(\S+)\sinitialized and serving traffic'],
        unless = [],
        commands = [ _notify_cmd.NotifyCmd( 
            message=r"\1 started and serving traffic"),],
      ),
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
    return "default"
    
  def description(self):
    """ Description for help """
    return "Typical plugin for Java style output"
    
class TestPlugin(_plugin.TestCommand):
  def setUp(self):
    """ Setup self.instance here """
    self.mo = monitoroutput.monitoroutput.MonitorOutput()
    self.instance = DefaultPlugin()
    self.mo.curplugin = self.instance
    
  def testSearches(self):
    lines = [
      'Started', "070419 19:07:11.861:I 40 [Thread-12] [com2.run] AXTE initialized and serving traffic"
    ]
    for name, line in lines:
      self.mo.replace_commands(name, [_plugin.FakeCommandPlugin(name)])
      out = self.mo.handle_line(line)
      self.assertEquals(name, out)

  def testWarning(self):
    line = "] WARNING: blabla"
    out = self.mo.handle_line(line)
    self.assertEquals('\033[0;34m] WARNING: blabla\033[0m', out)

  def testThreadWarning(self):
    line = 'Exception in thread "main" com.google.common.base.Flags$FlagUpdateError: '
    out = self.mo.handle_line(line)

  def testThreadWarning(self):
    out = self.mo.handle_exit()

if __name__ == "__main__":
  import unittest
  unittest.main()
