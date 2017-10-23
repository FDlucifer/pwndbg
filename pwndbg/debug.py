import gdb

_orig_execute = gdb.execute

def execute(*a, **kw):
    print("gdb.execute(%r, %r)" % (a, kw))
    return _orig_execute(*a, **kw)

gdb.execute = execute
