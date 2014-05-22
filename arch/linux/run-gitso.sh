#! /bin/bash

if test "$1" == "-h" -o "$1" == "--help"; then
    echo -e "Usage: ./run-gitso.sh [options]"
    echo -e "\tOptions:"
    echo -e "\t--have-wxpython:\tDisable wxPython library check"
    exit 0
fi


## Checking for x11vnc
if test ! "`which x11vnc`"; then
    echo -e "Error - x11vnc was not found on your system.\n"
    exit 1
fi

## Checking for wxpython
if test "$1" != "--have-wxpython"; then
    if test ! "`locate wxPython/lib`"; then
			echo -e "\nError - wxPython was not found on your system."
			echo -e "\nIf you know you have wxPython installed, use '--have-wxpython'.\n\tExample: ./run-gitso --have-wxpython\n"
			exit 1
    fi
else
    echo -e "\nBypassing wxpython check..."
fi

## Checking for vncviewer
if test ! "`which vncviewer`"; then
    echo -e "\nError - vncviewer was not found on your system.\n"
    exit 1
fi


echo -e "Starting Gitso..."
bin/gitso
