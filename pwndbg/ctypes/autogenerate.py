"""On-the fly GDB debugging symbol generation from ctypes structs."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ctypes

import pwndbg.typeinfo

TYPES = {
    ctypes.c_uint: 'uint32_t',

    ctypes.c_byte: 'uint8_t',
    ctypes.c_char: 'int8_t',
    ctypes.c_char_p: 'int8_t*',

    ctypes.c_double: 'double',
    ctypes.c_float: 'float',

    ctypes.c_int: 'int32_t',
    ctypes.c_int16: 'int16_t',
    ctypes.c_int32: 'int32_t',
    ctypes.c_int64: 'int64_t',
    ctypes.c_int8: 'int8_t',

    ctypes.c_long: 'long',
    ctypes.c_longdouble: 'long double',
    ctypes.c_longlong: 'long long',

    ctypes.c_short: 'short',

    ctypes.c_size_t: 'size_t',
    ctypes.c_ssize_t: 'ssize_t',

    ctypes.c_ubyte: 'uint8_t',
    ctypes.c_uint: 'uint32_t',
    ctypes.c_uint16: 'uint16_t',
    ctypes.c_uint32: 'uint32_t',
    ctypes.c_uint64: 'uint64_t',
    ctypes.c_uint8: 'uint8_t',

    ctypes.c_ulong: 'unsigned long',
    ctypes.c_ulonglong: 'unsigned long long',

    ctypes.c_ushort: 'unsigned short',

    ctypes.c_void_p: 'void *',
    ctypes.c_voidp: 'void *'
}

def convert_Structure_to_header(struct, converted=None):
    if not isinstance(struct, ctypes.Structure):
        assert ValueError("struct is not a ctypes.Structure: %r" % struct)

    offset = 0

    types_to_convert = []
    types_converted = converted or {}

    struct_name = struct.__name__

    lines = []
    lines.append("#include <stdint.h>")
    lines.append("typedef struct %s {" % struct_name)

    for fieldname, fieldtype in struct._fields_:
        array_length = 0
        attribs = getattr(struct, fieldname)

        # Handle arrays
        if hasattr(fieldtype, '_length_'):
            array_length = fieldtype._length_
            fieldtype = fieldtype._type_

        # Find the number of times to dereference, and extract
        # inner type.
        deref_count = 0

        while isinstance(fieldtype, ctypes._Pointer):
            derefs_count += 1
            fieldtype = fieldtype._type_

        # Handle the naming of the actual type, if it is a built-in
        # type or otherwise handled by stdint.h
        if fieldtype in TYPES:
            field_type_name = TYPES[fieldtype]

        # More complex type.
        # See if we have already loaded it in GDB, and if not then recurse.
        elif isinstance(fieldtype, ctypes.Structure):
            pwndbg.typeinfo.load()
            converted = convert_Structure_to_struct(fieldtype, types_converted)
            types_converted.append(converted)
            field_type_name = fieldtype.__name__
        else:
            print("Unknown type", fieldname, fieldtype)
            return None

        array_specifier = '' if not array_length else '[%i]' % array_length

        lines.append('\t%-20s %s%s;' % (field_type_name, fieldname, array_specifier))

    lines.append("} %s;" % struct_name)
    lines.append("%s __%s_instance;" % (struct_name, struct_name))

    return '\n'.join(lines)
