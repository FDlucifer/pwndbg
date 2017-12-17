import pytest

from pwndbg.services.misc import pwndbg_list_and_filter_commands


def test_show_super_assert():
    x = [1, 2, 3]
    assert x == [1, 2, 4]


def test_code_that_should_fail():
    with pytest.raises(ZeroDivisionError):
        1 / 0


def test_pwndbg_list_and_filter_commands_filter():
    assert pwndbg_list_and_filter_commands('stack') == [
        ('canary', 'Print out the current stack canary'),
        ('context', 'Print out the current register, instruction, and stack context.'),
        ('down', 'Select and print stack frame called by this one.'),
        ('retaddr', 'Print out the stack addresses that contain return addresses'),
        ('stack', 'dereferences on stack data with specified count and offset'),
        ('up', 'Select and print stack frame that called this one.')
    ]


def test_pwndbg_list_and_filter_commands_full_list():
    assert pwndbg_list_and_filter_commands('') == [
        ('address', "Windbg compatibility alias for 'vmmap' command."),
        ('arena', 'Prints out the main arena or the arena at the specified by address.'),
        ('arenas', 'Prints out allocated arenas'), ('argc', 'Prints out the number of arguments.'),
        ('args', 'Prints out the contents of argv.'), ('argv', 'Prints out the contents of argv.'),
        ('aslr', 'Inspect or modify ASLR status'), ('auxv', 'Print information from the Auxiliary ELF Vector.'),
        ('bc', 'Clear the breapoint with the specified index.'),
        ('bd', 'Disable the breapoint with the specified index.'),
        ('be', 'Enable the breapoint with the specified index.'),
        ('bins', 'Prints out the contents of the fastbins, unsortedbin, smallbins, and largebins from the'),
        ('bl', 'List breakpoints'), ('bp', 'Set a breakpoint at the specified address.'),
        ('canary', 'Print out the current stack canary'),
        ('checksec', 'Prints out the binary security settings. Attempts to call the binjitsu'),
        ('config', 'Shows pwndbg-specific configuration points'),
        ('configfile', 'Generates a configuration file for the current Pwndbg options'),
        ('context', 'Print out the current register, instruction, and stack context.'),
        ('cpsr', 'Print out the ARM CPSR register'), ('da', 'Dump a string at the specified address.'),
        ('db', 'Starting at the specified address, dump N bytes'), ('dc', None),
        ('dd', 'Starting at the specified address, dump N dwords'),
        ('dds', 'Dump pointers and symbols at the specified address.'),
        ('distance', 'Print the distance between the two arguments'),
        ('down', 'Select and print stack frame called by this one.'),
        ('dps', 'Dump pointers and symbols at the specified address.'),
        ('dq', 'Starting at the specified address, dump N qwords'),
        ('dqs', 'Dump pointers and symbols at the specified address.'),
        ('ds', 'Dump a string at the specified address.'), ('dt', 'Dump out information on a type (e.g. ucontext_t).'),
        ('dumpargs', 'Prints determined arguments for call instruction. Pass --all to see all possible arguments.'),
        ('dw', 'Starting at the specified address, dump N words'), ('eb', 'Write hex bytes at the specified address.'),
        ('ed', 'Write hex dwords at the specified address.'),
        ('elfheader', 'Prints the section mappings contained in the ELF header.'),
        ('emulate', 'Like nearpc, but will emulate instructions from the current $PC forward.'),
        ('entry', 'Set a breakpoint at the first instruction executed in'),
        ('entry_point', 'GDBINIT compatibility alias to print the entry point.'),
        ('env', 'Prints out the contents of the environment.'),
        ('environ', 'Prints out the contents of the environment.'),
        ('envp', 'Prints out the contents of the environment.'), ('eq', 'Write hex qwords at the specified address.'),
        ('errno', 'Converts errno (or argument) to its string representation.'),
        ('ew', 'Write hex words at the specified address.'), ('ez', 'Write a string at the specified address.'),
        ('eza', 'Write a string at the specified address.'),
        ('fastbins', 'Prints out the contents of the fastbins of the main arena or the arena'),
        ('find_fake_fast', 'Finds candidate fake fast chunks that will overlap with the specified'),
        ('fsbase', 'Prints out the FS base address.  See also $fsbase.'), ('getfile', None), ('getpid', None),
        ('go', "Windbg compatibility alias for 'continue' command."),
        ('got', 'Show the state of the Global Offset Table'),
        ('gotplt', 'Prints any symbols found in the .got.plt section if it exists.'),
        ('gsbase', 'Prints out the GS base address.  See also $gsbase.'),
        ('heap', 'Prints out all chunks in the main_arena, or the arena specified by `addr`.'),
        ('hexdump', 'Hexdumps data at the specified address (or at $sp)'),
        ('init', "GDBINIT compatibility alias for 'start' command."), ('j', "Synchronize IDA's cursor with GDB"),
        ('k', "Print a backtrace (alias 'bt')"), ('kd', 'Dump pointers and symbols at the specified address.'),
        ('largebins', 'Prints out the contents of the large bin of the main arena or the arena'),
        ('libs', "GDBINIT compatibility alias for 'libs' command."),
        ('lm', "Windbg compatibility alias for 'vmmap' command."),
        ('ln', 'List the symbols nearest to the provided value.'),
        ('main', "GDBINIT compatibility alias for 'main' command."),
        ('malloc_chunk', 'Prints out the malloc_chunk at the specified address.'),
        ('memfrob', 'memfrob(address, count)'), ('mp', 'Prints out the mp_ structure from glibc'),
        ('nearpc', 'Disassemble near a specified address.'), ('next_syscall', 'Breaks at the next syscall.'),
        ('nextcall', 'Breaks at the next call instruction'), ('nextjmp', 'Breaks at the next jump instruction'),
        ('nextjump', 'Breaks at the next jump instruction'),
        ('nextproginstr', 'Breaks at the next instruction that belongs to the running program'), ('nextret', None),
        ('nextsc', 'Breaks at the next syscall.'), ('pc', "Windbg compatibility alias for 'nextcall' command."),
        ('pdisass', "Compatibility layer for PEDA's pdisass command"), ('peb', None), ('pid', None),
        ('plt', 'Prints any symbols found in the .plt section if it exists.'),
        ('procinfo', 'Display information about the running process.'), ('pwndbg',
                                                                         'Prints out a list of all pwndbg commands. The list can be optionally filtered if filter_pattern is passed.'),
        ('r2', '.'), ('regs', 'Print out all registers and enhance the information.'),
        ('reinit_pwndbg', 'Makes pwndbg reinitialize all state.'), ('reload', None),
        ('retaddr', 'Print out the stack addresses that contain return addresses'),
        ('rop', "Dump ROP gadgets with Jon Salwan's ROPgadget tool."), ('ropgadget', None),
        ('ropper', 'ROP gadget search with ropper.'), ('save_ida', 'Save the IDA database'),
        ('search', 'Search memory for byte sequences, strings, pointers, and integer values'),
        ('smallbins', 'Prints out the contents of the small bin of the main arena or the arena'),
        ('so', 'Alias for stepover'),
        ('sstart', "GDBINIT compatibility alias for 'tbreak __libc_start_main; run' command."),
        ('stack', 'dereferences on stack data with specified count and offset'),
        ('start', 'Set a breakpoint at a convenient location in the binary,'),
        ('stepover', 'Sets a breakpoint on the instruction after this one'),
        ('telescope', 'Recursively dereferences pointers starting at the specified address'),
        ('theme', 'Shows pwndbg-specific theme configuration points'),
        ('themefile', 'Generates a configuration file for the current Pwndbg theme options'),
        ('top_chunk', 'Prints out the address of the top chunk of the main arena, or of the arena'),
        ('u', 'Starting at the specified address, disassemble'),
        ('unsortedbin', 'Prints out the contents of the unsorted bin of the main arena or the'),
        ('up', 'Select and print stack frame that called this one.'),
        ('version', 'Displays gdb, python and pwndbg versions.'),
        ('vmmap', 'Print virtual memory map pages. Results can be filtered by providing address/module name.'),
        ('vprot', "Windbg compatibility alias for 'vmmap' command."), ('xor', 'xor(address, key, count)')
    ]