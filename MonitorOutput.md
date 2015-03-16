# Introduction #

Waiting for your compile to finish or server to startup is boring. Having a program do it for you is cool!

![http://monitor-output.googlecode.com/svn/trunk/doc/notify-screenshot.png](http://monitor-output.googlecode.com/svn/trunk/doc/notify-screenshot.png)

How it works is you create a setup that searches for text in the output and when that text is detected it fires off a command.  The command can do anything including modifying the output as to make it appear different (ex. in color).

# How To Run #

The easiest way to run this in linux like systems is
```
myprogram 2>&1 | monitor-output
```
The "2>&1" part is optional, but useful, it'll also send stderr output to monitor-output.
If you want to monitor a log file you can run:
```
tail -f mylog.log | monitor-output
```
You can also ask monitor output to run the program for you, but I find it doesn't work quite the same so I advise against it for now.  Ex.
```
monitor-output myprogram
```

You can create various events by making "plugins" which need to live in the `python*/site-packages/monitor-output/monitoroutput/plugins` directory.  Any .py file in that directory that doesn't have an underscore at the start of the name will be loaded up as plugin.

You may have different plug-ins for different types of output, you can do this with::
```
myprogram 2>&1 | monitor-output --mop myplugin
```

The option --mop (for monitor-output plugin) which pick which plugin to use.  The default is to use the plugin called "default".

# Sample Plugin #

In order to make a plugin you need a little bit of Python experience.  You have to find the [plugins directory](FindingPluginsDir.md).  In that folder you create a python program with a filename that **doesn't** start with and underscore.

Here's a sample:
```
#!/usr/bin/env python
# -*- encoding: latin1 -*-

"""
Some Ccmment about your plugin
"""
import monitoroutput.monitoroutput
import _plugin
import _colorize_cmd
import _notify_cmd
import re

def create_plugin():
    return MyPlugin()

class MyPlugin(_plugin.MonitorPlugin):
    def __init__(self):
        _plugin.MonitorPlugin.__init__(self)

        self.events = [
          dict(
            name='Warning',
            greps = [ r'(.*\sWARNING:.*)'],
            unless = [],
            commands = [ _colorize_cmd.ColorizeCmd(color="Blue"),],
          ),
          dict(
            name='Error',
            params = re.IGNORECASE,
            greps = [ r'(.*\sERROR.*)'],
            unless = [r'ErrorClass', r'ErrorException'],
            commands = [ _notify_cmd.NotifyCmd(
                message="Error occured"),],
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
        return "My Plugin"

    def description(self):
        """ Description for help """
        return "Sample plugin"
```

  * In this sample we will turn the whole like blue if it has the word "WARNING" or "Warning", etc. in it.
  * Also any line that has the word "Error" in it will get a Gnome Popup via libnotify indicating an error occurred, unless the line has "ErrorClass" or "ErrorException" in it.
  * Finally, when the program exists it will notify the user as well.

# Commands #

Currently there is a limited number of commands you can call, although you are free to create more commands as necessary (and contribute back to the project)!

  * NotifyCmd
  * ColorizeCmd