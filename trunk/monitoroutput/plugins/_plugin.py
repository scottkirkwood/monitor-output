#!/usr/bin/env python
# -*- encoding: latin1 -*-
#
# Copyright 2007 Scott Kirkwood

import unittest

class ClipboardPlugin:
  def __init__(self):
    self.last_message = ''
    self.was_converted = False
    
  def message(self):
    """ Short message describing what happened 
    
    Returns: String or empty string (not None)
    """
    return self.last_message
    
  def converted(self):
    """ Was the last convet() call successfull? 
    
    Returns: True/False
    """
    return self.was_converted
    
  def _ret_result(self, message, sucess, text=''):
    self.last_message = message
    self.was_converted = sucess
    return text

  def name(self):
    """ This is the name that appears in the dialog """
    pass
    
  def description(self):
    """ This is long description that shows up in tool tips """
    pass
    
  def convert(self, text):
    """ This is the function that does the actual convertion """
  
class TestPlugin(unittest.TestCase):
  def setUp(self):
    """ Setup self.instance here """
    pass
    
  def verify_good_samples(self, good_samples, expected_ok = None):
    """ Verify that an array of (intput, expected-output) match
    Ex
    """
    for good_sample, expected in good_samples:
      results = self.instance.convert(good_sample)
      self.assertTrue(self.instance.converted())
      if expected_ok != None:
        if not self.instance.message().startswith(expected_ok):
          self.fail("Expected: " + expected_ok + " but got " + self.instance.message())
      self.assertEquals(expected, results)

  def verify_bad_samples(self, bad_samples):
    for bad_sample in bad_samples:
      results = self.instance.convert(bad_sample)
      self.assertFalse(self.instance.converted())
      self.assertEquals('', results)
    
