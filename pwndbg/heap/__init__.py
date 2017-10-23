#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pwndbg.heap
import pwndbg.symbol

current = None

# Since glibc uses ptmalloc by default, we will use it as our fall-back.
default = pwndbg.heap.ptmalloc.Heap

@pwndbg.events.new_objfile
def update():
    import pwndbg.heap.dlmalloc
    import pwndbg.heap.ptmalloc

    global current


    if pwndbg.symbol.address('ptmalloc_init'):
        current = pwndbg.heap.ptmalloc.Heap()

    elif pwndbg.symbol.address('dlfree'):
        current = pwndbg.heap.dlmalloc.Heap()

    else:
        current = default()
