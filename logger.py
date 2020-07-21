#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import logging

# ロガーの生成
def gene_logger(file):
  _logger = logging.getLogger(__name__)
  _logger.setLevel(10)
  target = os.path.join(os.path.dirname(__file__), file)
  fh = logging.FileHandler(target)
  _logger.addHandler(fh)
  formatter = logging.Formatter('%(asctime)s_%(filename)s:%(lineno)d:%(message)s')
  fh.setFormatter(formatter)
  return _logger
