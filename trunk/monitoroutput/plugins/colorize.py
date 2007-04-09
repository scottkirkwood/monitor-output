#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

import _plugin

def create_plugin():
  return ColorizePlugin()
  
class ColorizePlugin(_plugin.MonitorPlugin):
  def __init__(self):
    _plugin.MonitorPlugin.__init__(self)
    
  def name(self):
    """ This plugin's name """
    return "colorize"
    
  def description(self):
    """ Description for help """
    return "given a regex turn the text a certain color using ANSI text"
    
  def search(self):
    pass
  
class TestPlugin(_plugin.TestPlugin):
  def setUp(self):
    """ Setup self.instance here """
    self.instance = ColorizePlugin()
    
