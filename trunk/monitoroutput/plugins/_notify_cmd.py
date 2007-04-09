#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

import _plugin

class NotifyCmd(_plugin.CommandPlugin):
  def __init__(self, subject, message):
    self.subject = subject
    self.message = message
  
  def __call__(self, match, line):
    try:
      import pynotify
      
      if not pynotify.is_initted():
        pynotify.init('monitor-output-notify')
      self.notify = pynotify.Notification(self.subject, self.message)
      self.notify.show()
    except:
      import subprocess
      subprocess.call(['notify-send', '--expire-time=-1', 
          self.subject, self.message])
    return line

class TestCommand(_plugin.TestCommand):
  def setUp(self):
    """ Setup self.instance here """
    self.instance = NotifyCmd("Hey", "There")
    
  def testCommand(self):
    import re
    
    re_err = re.compile('Error')
    line  = "[Error]"
    match = re_err.search(line)
    ret = self.instance(match, line)
    self.assertEquals("[Error]", ret)

if __name__ == "__main__":
  import unittest
  unittest.main()
