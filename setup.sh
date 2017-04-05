#!/bin/bash
set -ex

PYTHON=''
INSTALLFLAGS=''

if [ "$1" == "--user" ] || (uname | grep -i Darwin &>/dev/null); then
    INSTALLFLAGS="--user"
else
    PYTHON="sudo "
fi

if uname | grep -i Linux &>/dev/null; then
    sudo apt-get update || true
    sudo apt-get -y install gdb python-dev python3-dev python-pip python3-pip libglib2.0-dev libc6-dbg

    if uname -m | grep x86_64 > /dev/null; then
        sudo apt-get install libc6-dbg:i386 || true
    fi
fi

if ! hash gdb; then
    echo 'Could not find gdb in $PATH'
    exit
fi

# Update all submodules
git submodule update --init --recursive

# Find the Python version used by GDB.
PYVER=$(gdb -batch -q --nx -ex 'pi import platform; print(".".join(platform.python_version_tuple()[:2]))')
PYTHON+=$(gdb -batch -q --nx -ex 'pi import sys; print(sys.executable)')
PYTHON+="${PYVER}"

# Make sure that pip is available
if ! ${PYTHON} -m pip -V; then
    ${PYTHON} -m ensurepip --upgrade
fi

# Upgrade pip itself
${PYTHON} -m pip install ${INSTALLFLAGS} --upgrade pip

# Install Python dependencies
${PYTHON} -m pip install ${INSTALLFLAGS} -Ur requirements.txt

# Load Pwndbg into GDB on every launch.
if ! grep pwndbg ~/.gdbinit &>/dev/null; then
    echo "source $PWD/gdbinit.py" >> ~/.gdbinit
fi
