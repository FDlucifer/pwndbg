#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ctypes
import gdb

import pwndbg.ctypes
import pwndbg.events
import pwndbg.typeinfo

import pwndbg.heap.baseheap

class malloc_chunk(pwndbg.ctypes.Structure):
    _fields_ = [ ('prev_size', pwndbg.ctypes.size_t),
                 ('size', pwndbg.ctypes.size_t) ]

class DlMalloc(pwndbg.heap.baseheap.BaseHeap):
    def __init__(self, arena=None, mp=None):
        self._arena = None
        self._mp = None

