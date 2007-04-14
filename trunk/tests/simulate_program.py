#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

import sys
import time
import random

lines = """This is a sample of a program
that outputs slowly, sometimes not even a complete lines
Some lines will have error in them
And may cause a event to occur
"""


def output_slowly(lines):
  out = sys.stdout
  random.seed()
  
  while len(lines) > 0:
    bytes = random.randint(1, 30)
    sec_sleep = random.randint(0, 2)
    chunk = lines[:bytes]
    out.write(chunk)
    out.flush()
    time.sleep(sec_sleep)
    lines = lines[bytes:]
      
if __name__ == "__main__":
  output_slowly(lines)
