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