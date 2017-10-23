#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import gdb

import pwndbg.events
import pwndbg.memory
import pwndbg.symbol

class Range(object):
    """Base class for common operations about memory ranges."""
    def __init__(self, address, size=0):
        self.address = address
        self.size = size

    def __contains__(self, address):
        return self.address <= address <= (self.address + self.size)

    @property
    def contents(self):
        """Contents of the heap allocation"""
        return pwndbg.memory.read(self.address, self.size)


class Metadata(Range):
    """Base class which describes a heap allocation"""
    def __init__(self, address, size=0, free=False):
        super(Allocation, self).__init__(address,size)

    @property
    def free(self):
        """Whether the allocation described by this metadata is free"""
        return self.get_free()

    @property
    def allocation(self):
        """Allocation described by the heap metadata."""
        return self.get_metadata()

    def get_allocation(self):
        """Heap-specific extension point for retrieving the allocation for a metadata"""
        raise NotImplementedError()

    def get_free(self):
        """Heap-specific extension point for whether or not the metadata says the allocaiton is free"""


class Allocation(Range):
    """Base class which describes a memory range in the heap"""
    @property
    def free(self):
        return self.metadata.free

    @property
    def metadata(self):
        """Metadata for the heap allocation"""
        return self.get_metadata()

    def get_metadata(self):
        """Heap-specific extension point for retrieving the metadata for an allocation"""
        raise NotImplementedError()

    def __contains__(self, address):
        return self.address <= address <= (self.address + self.size)

class BaseHeap(object):
    """Heap abstraction layer."""

    def allocation(self, address):
        """Get the Allocation which is contained at the specified address"""

    def breakpoint(self, event, *args, **kwargs):
        """Enables breakpoints on the specific event.

        Arguments:
            event(str): One of 'alloc','realloc','free'
            args: List of arguments to pass to ``gdb.Breakpoint``
            kwargs: Dict of arguments to pass to ``gdb.Breakpoint``

        Returns:
            A list of gdb.Breakpoint objects.
        """
        valid_events = ('alloc', 'realloc', 'free')
        if event not in :
            raise ValueError("event must be one of %r, got %r" % (valid_events, event))

        names = {
            'alloc': ['malloc', 'calloc'],
            'free': ['free'],
            'realloc': ['realloc'],
        }

        breakpoints = []

        for name in names[event]:
            breakpoints.append(gdb.Breakpoint(name, *args, **kwargs))

        return breakpoints

    def summarize(self, address, **kwargs):
        """Returns a textual summary of the specified address.

        Arguments:
            address(int): Address of the heap block to summarize.
            kwargs(dict): Extra arguments for the heap-specific allocator.

        Returns:
            A string.
        """
        return self._summarize(address, **kwargs)

    def _summarize(self, address, **kwargs):
        """Allocator-specific implementation for summarize should overload this function."""
        raise NotImplementedError()

    def size(self, address):
        """Returns the total size of the allocation containing 'address',
        including any internal metadata.

        Arguments:
            address(int): Address to look up

        Returns:
            Size, in bytes.
        """
        try:
            return self._size(address)
        except NotImplementedError:
            return self.meta_size(address) + self.usable_size(address)

    def _size(self, address, **kwargs):
        """Allocator-specific implementation for size should overload this function."""
        raise NotImplementedError()

    def meta_size(self, address):
        """Returns the size of the metadata describing the allocation

        Arguments:
            address(int): Address to look up

        Returns:
            Size, in bytes.
        """
        raise NotImplementedError()

    def meta_for_user(self, user_address):
        """Returns the address of the metadata for the specified user allocation.

        Arguments:
            user_address(int): Address to look up

        Returns:
            Address of the metadata.
        """
        raise NotImplementedError()

    def user_for_meta(self, meta_address):
        """Returns the address of the metadata for the specified user allocation.

        Arguments:
            meta_address(int): Address to look up

        Returns:
            Address of the metadata.
        """
        raise NotImplementedError()

    def usable_size(self, address):
        """Returns the total size of the allocation containing 'address',
        including any internal metadata.

        Arguments:
            address(int): Address to look up

        Returns:
            Size, in bytes.
        """
        raise NotImplementedError()

    def usable_address(self, address):
        """Returns the first byte available to the user, in the allocaiton
        containing the provided address.

        Arguments:
            address(int): Address to look up

        Returns:
            Size, in bytes.
        """
        raise NotImplementedError()

    def in_use(self, address):
        """Returns whether or not the allocation (if any) containing the
        provided address is in use.

        Arguments:
            address(int): Address to look up

        Returns:
            True if the address is in use.
            False if the address is free.
            None if the address is unknown.
        """
        free = self.is_free(addres)
        if free == False:
            return True
        if free == True:
            return False
        return None

    def is_free(self, address):
        """Returns whether or not the allocation (if any) containing the
        provided address is free.

        Arguments:
            address(int): Address to look up

        Returns:
            True if the address is free.
            False if the address is in use.
            None if the address is unknown.
        """
        raise NotImplementedError()

    def containing(self, address):
        """Returns the address of the allocation which contains 'address'.

        Arguments:
            address(int): Address to look up.

        Returns:
            An integer (address).
        """
        raise NotImplementedError()

    def next(self, address):
        """Returns the address of the allocation which follows the provided one

        Note:
            Result should be linear and ordered.  Allocators which implement linked
            lists will need to figure out what comes after this one.
        """
        raise NotImplementedError()

    def prev(self, adddress):
        """Returns the address of the allocation which precedes the provided one

        Note:
            Result should be linear and ordered.  Allocators which implement linked
            lists will need to figure out what comes after this one.
        """
        raise NotImplementedError()

    def flags()
