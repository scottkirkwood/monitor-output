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
import select
import subprocess
import getopt

class MonitorOutput:
  def __init__(self):
    self.args = ['cat', 'test_message.txt']
  
  def run(self, arguments):
    p = subprocess.Popen(' '.join(self.args), 
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
        close_fds=True, shell=True)
        
    output = p.stdout
    
    while True:
      line = output.readline()
      if not line:
        self.handle_exit()
        break
      line = self.handle_line(line)
      sys.stdout.write(line)

  def monitor_stdin(self):
    intput = sys.stdin
    
    while True:
      line = intput.readline()
      if not line:
        break
      line = self.handle_line(line)
      sys.stdout.write(line)

  def handle_line(self, line):
    for event in self.curplugin.events:
      match = self.search(event, line)
      if match:
        line = self.run_events(event, match, line)
    return line

  def handle_exit(self):
    for event in self.curplugin.events:
      if 'event' in event and event['event'].lower().startswith('exit'):
        self.run_events(event, None, None)

  def select_plugin(self):
    optlist, self.args = getopt.getops(sys.argv, '', ["--mo"]):

    tofind = 'default'
    if len(optlist) > 0:
      if optlist[0][0] == '-mo':
        tofind = optlist[0][1]
    
    for plugin in self.MonitorPlugins:
      if plugin.get('name', '') == tofind:
        self.curplugin = plugin
        return
    
    self.curplugin = self.MonitorPlugins[0]
  
  def replace_commands(self, event_name, new_commands):
    for event in self.curplugin.events:
      if 'name' in event and event['name'] == event_name:
        event['commands'] = new_commands
    
  def search(self, event, line):
    """ Returns true if part matches 
    
    Here we should concat the regexes and memoize it for speed
    """
    found_groups = None
    if not 'greps' in event:
      return None
    
    if 'compile_regex' not in event:
      grep = '|'.join(event['greps'])
      event['compile_regex'] = re.compile(grep, event.get('params', 0))
    
    return  event['compile_regex'].search(line)
    
  def run_events(self, event, groups, line):
    """ Execute the event, possibly modifying the line """
    for cmd in event['commands']:
      line = cmd(groups, line)
    return line

  def find_modules(self):
    self.MonitorPlugins = []

    pluginfiles = self._GetPluginFiles()
    for filename in pluginfiles:
      if filename.endswith('.py') \
          and not filename.startswith('_'):
        import_text = 'plugins.'  + filename.replace('.py', '')
        self.import_plugin(import_text)

  def import_plugin(self, import_text):
    import plugins
    
    print import_text
    try:
      __import__('monitoroutput.' + import_text)
    except:
      __import__(import_text) # This works when developing
    self.MonitorPlugins.append(eval(import_text + '.create_plugin()'))
  
  def _GetPluginFiles(self):
    import os
    import plugins
    
    plugindir = os.path.join(re.sub('__init__.py.?', '', plugins.__file__))
    ret = os.listdir(plugindir)
    return ret

def parse_command_line():
    monitor_output = MonitorOutput()
    monitor_output.find_modules()
    monitor_output.select_plugin()
    
    if len(sys.argv) == 1 or (len(sys.argv) >  1 and sys.argv[1] == '-o'):
      monitor_output.monitor_stdin()
    else:
      monitor_output.run(sys.argv)

if __name__ == "__main__":
    parse_command_line()
