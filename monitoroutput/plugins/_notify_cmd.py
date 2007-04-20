#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

import _plugin

class NotifyCmd(_plugin.CommandPlugin):
  def __init__(self, message, subject = "Monitor Output"):
    self.subject = subject
    self.message = message
  
  def __call__(self, match, line):
    if match != None:
      message = match.expand(self.message)
    else:
      message = self.message
    
    try:
      import pynotify
      
      if not pynotify.is_initted():
        pynotify.init('monitor-output-notify')
      
      #TODO(scottkirkwood): incresae the expire time.
      self.notify = pynotify.Notification(self.subject, message)
      self.notify.show()
    except:
      import subprocess
      
      # The man page lies, it's not in seconds but milliseconds
      subprocess.call(['notify-send', '--expire-time', '200000', 
          self.subject, message])
    return line

class TestCommand(_plugin.TestCommand):
  def setUp(self):
    """ Setup self.instance here """
    self.instance = NotifyCmd(r"\1 is fine, thanks.")
    
  def testCommand(self):
    import re
    
    re_err = re.compile(r'Hi (\S+) how are you?')
    line  = "Hi Bob how are you?"
    match = re_err.search(line)
    ret = self.instance(match, line)

if __name__ == "__main__":
  import unittest
  unittest.main()
